<template>
	<div class="flex flex-row gap-4">
				<div
			v-for="section in _fields"
			:key="section.label"
			:class="
				sections.length == 2
					? 'section first:border-t-0 first:pt-0 w-1/2'
					: 'section first:border-t-0 first:pt-0 w-full'
			"
		>
			<div v-for="field in section.fields" :key="field.name" class="mb-4">
				<div v-if="field.type === 'Attach' && isPdfFile(data[field.name])">
					<iframe
						v-if="data[field.name]"
						:src="data[field.name]"
						class="w-full h-[600px] border border-gray-200"
						frameborder="0"
					></iframe>

					<!-- Fallback message if iframe cannot render -->
					<div v-else class="text-gray-500 mt-2">
						{{ __("Trình duyệt của bạn không hỗ trợ xem PDF trực tiếp. Hãy tải file tại đây:") }}
						<a :href="data[field.name]" target="_blank" class="text-blue-600 underline">
							{{ __("Tải File") }}
						</a>
					</div>
				</div>
			</div>
			<div
				v-if="!section.hideLabel"
				class="flex h-7 mb-3 max-w-fit cursor-pointer items-center gap-2 text-base font-semibold leading-5 hidden"
			>
				{{ section.label }}
			</div>
			<div
				class="grid gap-4"
				:class="section.columns ? 'grid-cols-' + section.columns : 'grid-cols-1 sm:grid-cols-1'"
			>
				<div
					v-for="field in section.fields"
					:class="[field.hidden && 'hidden']"
					:key="field.name"
				>
					<div
						class="settings-field"
						v-if="
							(field.type == 'Check' ||
								(field.read_only && data[field.name]) ||
								!field.read_only ||
								!field.hidden)
							
						"
					>
						<div
							v-if="field.type != 'Check' && field.type != 'Table'"
							class="mb-2 text-sm text-gray-600"
						>
							{{ __(field.label) }}
							<span
								class="text-red-500"
								v-if="
									field.mandatory || (field.mandatory_depends_on && field.mandatory_via_depends_on)
								"
								>*</span
							>
						</div>
						<FormControl
							v-if="field.read_only && field.type !== 'Check'"
							type="text"
							:placeholder="getPlaceholder(field)"
							v-model="data[field.name]"
							:disabled="Boolean(field.read_only)"
							:hidden="Boolean(field.hidden)"
						/>
						<FormControl
							v-else-if="field.type === 'Select'"
							type="select"
							class="form-control"
							:class="field.prefix ? 'prefix' : ''"
							:options="field.options"
							v-model="data[field.name]"
							:placeholder="getPlaceholder(field)"
							:disabled="Boolean(field.read_only)"
							:hidden="Boolean(field.hidden)"
						>
							<template v-if="field.prefix" #prefix>
								<IndicatorIcon :class="field.prefix" />
							</template>
						</FormControl>
						<div v-else-if="field.type == 'Check'" class="flex items-center gap-2">
							<FormControl
								class="form-control"
								type="checkbox"
								v-model="data[field.name]"
								@change="(e) => (data[field.name] = e.target.checked)"
								:disabled="Boolean(field.read_only)"
								:hidden="Boolean(field.hidden)"
							/>
							<label class="text-sm text-gray-600" @click="data[field.name] = !data[field.name]">
								{{ __(field.label) }}
								<span class="text-red-500" v-if="field.mandatory">*</span>
							</label>
						</div>
						<div class="flex gap-1" v-else-if="field.type === 'Link'">
							<Link
								class="form-control flex-1"
								:value="data[field.name]"
								:doctype="field.options"
								:filters="field.filters"
								@change="(v) => (data[field.name] = v)"
								:placeholder="getPlaceholder(field)"
								:onCreate="field.create"
							/>
							<Button
								v-if="data[field.name] && field.edit"
								class="shrink-0"
								:label="__('Edit')"
								@click="field.edit(data[field.name])"
							>
								<template #prefix>
									<EditIcon class="h-4 w-4" />
								</template>
							</Button>
						</div>
						<div class="flex gap-1" v-else-if="field.type === 'Table MultiSelect'">
							<MultipleSelect
								class="form-control flex-1"
								:value="data.child_tables[field.name]"
								:doctype="field.options"
								:filters="field.filters"
								@change="(v) => updateMultiSelect()"
								:placeholder="getPlaceholder(field)"
								:onCreate="field.create"
								:parentDoc="props.doctype"
								:name="field.name"
								:parentName="props.employeeId"
							/>
							<Button
								v-if="data[field.name] && field.edit"
								class="shrink-0"
								:label="__('Edit')"
								@click="field.edit(data[field.name])"
							>
								<template #prefix>
									<EditIcon class="h-4 w-4" />
								</template>
							</Button>
						</div>

						<Link
							v-else-if="field.type === 'User'"
							class="form-control"
							:value="getUser(data[field.name]).full_name"
							:doctype="field.options"
							:filters="field.filters"
							@change="(v) => (data[field.name] = v)"
							:placeholder="getPlaceholder(field)"
							:hideMe="true"
						>
							<template #prefix>
								<UserAvatar class="mr-2" :user="data[field.name]" size="sm" />
							</template>
							<template #item-prefix="{ option }">
								<UserAvatar class="mr-2" :user="option.value" size="sm" />
							</template>
							<template #item-label="{ option }">
								<Tooltip :text="option.value">
									<div class="cursor-pointer">
										{{ getUser(option.value).full_name }}
									</div>
								</Tooltip>
							</template>
						</Link>
						<div v-else-if="field.type === 'Dropdown'">
							<NestedPopover>
								<template #target="{ open }">
									<Button
										:label="data[field.name]"
										class="dropdown-button flex w-full items-center justify-between rounded border border-gray-100 bg-gray-100 px-2 py-1.5 text-base text-gray-800 placeholder-gray-500 transition-colors hover:border-gray-200 hover:bg-gray-200 focus:border-gray-500 focus:bg-white focus:shadow-sm focus:outline-none focus:ring-0 focus-visible:ring-2 focus-visible:ring-gray-400"
									>
										<div class="truncate">{{ data[field.name] }}</div>
										<template #suffix>
											<FeatherIcon
												:name="open ? 'chevron-up' : 'chevron-down'"
												class="h-4 text-gray-600"
											/>
										</template>
									</Button>
								</template>
								<template #body>
									<div
										v-if="field.type != 'Table'"
										class="my-2 space-y-1.5 divide-y rounded-lg border border-gray-100 bg-white p-1.5 shadow-xl"
									>
										<div>
											<DropdownItem
												v-if="field.options?.length"
												v-for="option in field.options"
												:key="option.name"
												:option="option"
											/>
											<div v-else>
												<div class="p-1.5 px-7 text-base text-gray-500">
													{{ __("No {0} Available", [field.label]) }}
												</div>
											</div>
										</div>
										<div class="pt-1.5">
											<Button
												variant="ghost"
												class="w-full !justify-start"
												:label="__('Create New')"
												@click="field.create()"
											>
												<template #prefix>
													<FeatherIcon name="plus" class="h-4" />
												</template>
											</Button>
										</div>
									</div>
								</template>
							</NestedPopover>
						</div>
						<DateTimePicker
							v-else-if="field.type === 'Datetime'"
							v-model="data[field.name]"
							:placeholder="getPlaceholder(field)"
							input-class="border-none"
						/>
						<DatePicker
							v-else-if="field.type === 'Date'"
							v-model="data[field.name]"
							:placeholder="getPlaceholder(field)"
							input-class="border-none"
							
						/>
						<FormControl
							v-else-if="['Small Text', 'Text', 'Long Text'].includes(field.type)"
							type="textarea"
							:placeholder="getPlaceholder(field)"
							v-model="data[field.name]"
							:disabled="Boolean(field.read_only)"
							:hidden="Boolean(field.hidden)"
						/>
						<FormControl
							v-else-if="['Int'].includes(field.type)"
							type="number"
							:placeholder="getPlaceholder(field)"
							v-model="data[field.name]"
							:disabled="Boolean(field.read_only)"
							:hidden="Boolean(field.hidden)"
						/>
						<FormControl
							v-else-if="field.type === 'Table'"
							class="hidden"
							type="number"
							:placeholder="getPlaceholder(field)"
							v-model="data[field.name]"
							:hidden="Boolean(field.hidden)"
						/>
						<StarRating
							v-else-if="field.type === 'Rating'"
							:rating="data[field.name]"
							:static="false"
							@update:rating="(rating) => (console.log(rating), (data[field.name] = rating))"
						/>
						<TextEditor
							v-else-if="field.type === 'Text Editor'"
							ref="content"
							variant="outline"
							:class="'w-full'"
							:content="data[field.name]"
							:placeholder="getPlaceholder(field)"
							:bubbleMenu="true"
							:fixedMenu="true"
							@change="(content) => (data[field.name] = content)"
							editor-class="!prose-sm !w-full overflow-auto !max-w-full min-h-[180px] max-h-80 py-1.5 px-2 rounded border border-gray-300 bg-white hover:border-gray-400 hover:shadow-sm focus:bg-white focus:border-gray-500 focus:shadow-sm focus:ring-0 focus-visible:ring-2 focus-visible:ring-gray-400 text-gray-800 transition-colors"
						/>
						<FileUploader
							v-else-if="field.type === 'Attach'"
							:fileTypes="['files/*']"
							:upload-args="{
								doctype: props.doctype,
								docname: props.employeeId,
								private: false,
							}"
							v-model="data[field.name]"
							@success="(file) => handleFileUploadSuccess(file, field.name)"
						>
							<template
								v-slot="{
									file,
									uploading,
									progress,
									uploaded,
									message,
									error,  
									total,
									success,
									openFileSelector,
								}"
							>
								<div class="flex items-center gap-4">
									<!-- Hiển thị tên file nếu có -->
									<div v-if="data[field.name]" class="text-gray-700 truncate max-w-xs">
										<a :href="data[field.name]" target="_blank" class="text-blue-600 underline">
											{{ data[field.name].split("/").pop() }}
											<!-- Lấy tên file -->
										</a>
										<!-- Nút Clear
										<Button variant="ghost" @click="clearFile(field.name)" class="text-red-500">
											Clear
										</Button> -->
									</div>
									<!-- Nút Upload -->
									<Button variant="ghost" @click="openFileSelector()" :loading="uploading">
										<div class="flex gap-2">
											{{ uploading ? `Uploading ${progress}%` : "Upload File" }}
											<AttachmentIcon class="h-4" />
										</div>
									</Button>
								</div>
							</template>
						</FileUploader>
						<FormControl
							v-else
							type="text"
							:placeholder="getPlaceholder(field)"
							v-model="data[field.name]"
							:disabled="Boolean(field.read_only)"
							:hidden="Boolean(field.hidden)"
							
						/>

						<div class="flex flex-col gap-2" v-if="!props.isCreateModal">
							<div class="flex justify-between" v-if="field.type == 'Table'">
								<span class="font-semibold text-lg mb-4">{{ field.label }}</span>
								<Button
									:variant="'solid'"
									:ref_for="true"
									theme="gray"
									size="sm"
									label="Button"
									:loading="false"
									:loadingText="null"
									:disabled="false"
									:link="null"
									@click="() => showModalAddChildRecords(field.options, field.name)"
								>
									Thêm
								</Button>
							</div>
							<ListView
								v-if="
									field.type == 'Table' &&
									getTableColumns(field.options)?.length > 0 &&
									getTableRows(field.options)?.length > 0
								"
								:columns="getTableColumns(field.options)"
								:rows="getTableRows(field.options)"
								:options="{
									selectable: false,
									showTooltip: false,
									resizeColumn: true,
								}"
								row-key="id"
							>
								<ListHeader>
									<ListHeaderItem v-for="column in columns" :key="column.id" :item="column">
									</ListHeaderItem>
								</ListHeader>
								<ListRows
									:rows="getTableRows(field.options)"
									v-slot="{ idx, column, item, row }"
									class="relative"
									@setChildRecord="(row) => setChildRecord(row, field.name, field.options)"
									@deleteRecord="(row) => deleteRecord(row, field.name, field.options)"
								>
									<ListRowItem :item="item" class="">
										<template #default="{ label }">
											<div
												class="truncate text-base"
												@click="
													(event) => {
														createTableResource(field.options, props.employeeId, true, row.id)
													}
												"
											>
												<StarRating
													v-if="column.fieldtype === 'Rating'"
													:rating="item"
													:static="true"
												/>
												<span v-else>{{ label }}</span>
											</div>
										</template>
									</ListRowItem>
								</ListRows>
							</ListView>
							<div
								v-if="
									field.type == 'Table' &&
									(getTableColumns(field.options)?.length == 0 ||
										getTableRows(field.options)?.length == 0)
								"
							>
								<div
									class="flex flex-1 flex-col items-center justify-center gap-3 text-xl font-medium text-gray-500"
								>
									<svg
										width="16"
										height="16"
										viewBox="0 0 16 16"
										fill="none"
										xmlns="http://www.w3.org/2000/svg"
										class="text-gray-500 h-10 w-10"
									>
										<path
											fill-rule="evenodd"
											clip-rule="evenodd"
											d="M3.99707 14H11.9971C12.8255 14 13.4971 13.3284 13.4971 12.5V6.49988L12 6.49989C10.6193 6.4999 9.5 5.38061 9.5 3.99989V2H3.99707C3.16864 2 2.49707 2.67157 2.49707 3.5V12.5C2.49707 13.3284 3.16864 14 3.99707 14ZM13.8291 4.2806C14.1476 4.62366 14.3612 5.04668 14.4502 5.49987L14.4968 5.49987L14.4968 5.94777L14.4971 5.98173V12.5C14.4971 13.8807 13.3778 15 11.9971 15H3.99707C2.61636 15 1.49707 13.8807 1.49707 12.5V3.5C1.49707 2.11929 2.61636 1 3.99707 1H9.69261C10.3878 1 11.0516 1.28945 11.5246 1.79887L13.8291 4.2806ZM12 5.49989L13.4176 5.49988C13.3502 5.30132 13.2414 5.11735 13.0963 4.96105L10.7918 2.47932C10.7044 2.38525 10.6063 2.30368 10.5 2.23582V3.99989C10.5 4.82832 11.1716 5.4999 12 5.49989ZM5 11C4.72386 11 4.5 11.2239 4.5 11.5C4.5 11.7761 4.72386 12 5 12H8C8.27614 12 8.5 11.7761 8.5 11.5C8.5 11.2239 8.27614 11 8 11H5ZM10 9.5H5H4.75C4.47386 9.5 4.25 9.27614 4.25 9C4.25 8.72386 4.47386 8.5 4.75 8.5H5H10H11.25C11.5261 8.5 11.75 8.72386 11.75 9C11.75 9.27614 11.5261 9.5 11.25 9.5H10Z"
											fill="currentColor"
										></path>
									</svg>
									<span>Không có dữ liệu</span>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
	<CreateChildRecordModal
		v-model="showModalAddChildRecord"
		:fields="ChildTableField"
		:doctype="DoctypeActive"
		:parentName="props.doctype"
		:parentfield="parentFieldActive"
		:parent="props.employeeId"
		:options="{
			redirect: false,
			afterInsert: (doc) => createTableResource(DoctypeActive, props.employeeId),
		}"
		:detailChildTable="ChildRecordDetail"
		@updateRecord="(data) => handleUpdateRecord(data)"
	/>
</template>

<script setup>
import EditIcon from "@/components/Icons/EditIcon.vue"
import NestedPopover from "@/components/NestedPopover.vue"
import DropdownItem from "@/components/DropdownItem.vue"
import IndicatorIcon from "@/components/Icons/IndicatorIcon.vue"
import AttachmentIcon from "@/components/Icons/AttachmentIcon.vue"
import UserAvatar from "@/components/UserAvatar.vue"
import StarRating from "@/components/StarRating.vue"
import Link from "@/components/Controls/Link.vue"
import ListRows from "@/components/frappe-ui-custom/ListViewCustom/ListRows.vue"
// import ChildTableListView from "../components/ListViews/ChildTableListView.vue"
import CreateChildRecordModal from "../components/Modals/CreateChildRecordModal.vue"
import ListBulkActions from "@/components/ListBulkActions.vue"
import MultipleSelect from "@/components/Controls/MultipleSelect.vue"
import { usersStore } from "@/stores/users"
import {
	Tooltip,
	DatePicker,
	DateTimePicker,
	createResource,
	createListResource,
	Dropdown,
	Avatar,
	Tabs,
	usePageMeta,
	FileUploader,
	Button,
	ListView,
	ListRowItem,
	ListHeader,
	ListHeaderItem,
	TextEditor,
} from "frappe-ui"
import { createToast } from '@/utils'
import { ref, computed, h, onMounted, onBeforeUnmount, reactive, watch } from "vue"
const { getUser } = usersStore()

const props = defineProps({
	sections: Array,
	data: Object,
	employeeId: {
		type: String,
		required: true,
	},
	doctype: {
		type: String,
		required: false,
	},
	tableFields: {
		type: Object,
		required: true,
	},
	tableData: {
		type: Object,
		required: true,
	},
	dynamicTables: {
		type: Array,
		required: true, // Mảng danh sách bảng hoặc Doctype
	},
	isCreateModal: {
		type: Boolean,
		default: false,
	},
})

const emit = defineEmits(["updateRecord"])

const showModalAddChildRecord = ref(false)
const ChildTableField = ref([])
const ChildRecordDetail = ref(null)
const DoctypeActive = ref("")
const parentFieldActive = ref("")
const updateRecord = ref("")
const _fields = ref([])

watch(
	() => props.data, // Theo dõi props.data
	(newData) => {
		const transformed_sections = props.sections?.map((section) => {
			// Tạo một section mới giữ nguyên cấu trúc
			const transformed_section = {
				...section,
				fields: section.fields?.map((field) => {
					const df = field?.all_properties

					// Đánh giá phụ thuộc
					if (df?.depends_on) evaluate_depends_on(df.depends_on, field)
					if (df?.read_only_depends_on)
						evaluate_read_only_depend_on(df.read_only_depends_on, field)
					if (df?.mandatory_depends_on)
						evaluate_mandatory_depend_on(df.mandatory_depends_on, field)

					// Trả về field đã được biến đổi
					return {
						...field,
						filters: df?.link_filters && JSON.parse(df.link_filters),
						placeholder: field.placeholder || field.label,
					}
				}),
			}

			return transformed_section
		})

		// Cập nhật _fields với dữ liệu mới
		_fields.value = transformed_sections
	},
	{ deep: true, immediate: true } // Theo dõi sâu và chạy ngay khi khởi tạo
)
// Hàm đánh gias read only
function evaluate_read_only_depend_on(expression, field) {
	if (expression.substr(0, 5) == "eval:") {
		try {
			let out = evaluate(expression.substr(5), { doc: props.data })

			field.read_only = out ? true : false
		} catch (e) {
			console.error(e)
		}
	}
}

// Hàm đánh giá phụ thuộc bắt buộc
function evaluate_mandatory_depend_on(expression, field) {
	if (expression.substr(0, 5) == "eval:") {
		try {
			let out = evaluate(expression.substr(5), { doc: props.data })

			field.mandatory = out ? true : false
		} catch (e) {
			console.error(e)
		}
	}
}

function evaluate_depends_on(expression, field) {
	if (expression.substr(0, 5) == "eval:") {
		try {
			let out = evaluate(expression.substr(5), { doc: props.data })

			field.hidden = out ? false : true
		} catch (e) {
			console.error(e)
		}
	}
}

function evaluate(code, context = {}) {
	let variable_names = Object.keys(context)
	let variables = Object.values(context)
	code = `let out = ${code}; return out`
	try {
		let expression_function = new Function(...variable_names, code)

		return expression_function(...variables)
	} catch (error) {

		console.error(code)
		throw error
	}
}

function isPdfFile(fileUrl) {
	// Kiểm tra xem URL có kết thúc bằng ".pdf" hay không
	return fileUrl?.toLowerCase()?.endsWith(".pdf")
}

const handleUpdateRecord = (data) => {

	updateChildRecord(
		props.doctype,
		props.employeeId,
		data?.parentField,
		updateRecord.value,
		data?.infoEmployee,
		data?.doctype
	)
}

const fetchTableResources = () => {
	props.dynamicTables?.forEach((doctype) => {
		createTableResource(doctype, props.employeeId)
	})
}

function createTableResource(doctype, name, getAll, filterId = null) {
	const fields = props.tableFields[doctype] || []

	const filters = filterId
		? { id: filterId } // Proper JSON object if filtering by ID
		: {}
	return createResource({
		url: "xxx.api.childrecord.get_dynamic_data",
		params: {
			doctype: doctype, // Doctype con
			parent_name: name, // ID của bản ghi cha
			parenttype: props.doctype, // Doctype cha
			fields: getAll ? "*" : fields.length > 0 ? JSON.stringify(fields) : null, // Truyền danh sách các trường (nếu có)
			filters: filters,
		},
		onSuccess: (response) => {
			if (!getAll) {
				props.tableData[doctype].columns = response.columns // Lưu cột của bảng vào state
				props.tableData[doctype].rows = response.rows // Lưu dữ liệu hàng vào state
			} else {
				console.log(response)
			}
		},
		onError: (error) => {
			console.error(`Lỗi khi tải dữ liệu cho ${doctype}:`, error)
		},
		auto: true, // Tự động gọi API khi hàm được gọi
	})
}

onMounted(() => {
	if (!props.isCreateModal) {
		fetchTableResources()
	}
})

const getPlaceholder = (field) => {
	if (field.placeholder) {
		return __(field.placeholder)
	}
	if (["Select", "Link"].includes(field.type)) {
		return __("Select {0}", [__(field.label)])
	} else {
		return __("Enter {0}", [__(field.label)])
	}
}

async function showModalAddChildRecords(doctype, name) {
	showModalAddChildRecord.value = true
	ChildRecordDetail.value = null
	await getFieldChildTable(doctype)
	DoctypeActive.value = doctype
	parentFieldActive.value = name
}
// Hàm lấy columns cho bảng
function getTableColumns(doctype) {
	return props.tableData[doctype]?.columns || []
}

// Hàm lấy rows cho bảng
function getTableRows(doctype) {
	return props.tableData[doctype]?.rows || []
}

async function setChildRecord(data, name, doctype) {
	updateRecord.value = data
	await getChildRecord(props.doctype, props.employeeId, name, data)
	await getFieldChildTable(doctype)
	showModalAddChildRecord.value = true
}

function getChildRecord(parent_doctype, parent_name, child_table_field, child_name) {
	return createResource({
		url: "xxx.api.childrecord.get_child_record", // Đường dẫn đến API trong backend
		params: {
			parent_doctype: parent_doctype, // Doctype của bản ghi cha
			parent_name: parent_name, // Tên bản ghi cha
			child_table_field: child_table_field, // Trường bảng con trong tài liệu cha
			child_name: child_name, // Tên của bản ghi con cần lấy
		},
		onSuccess: (response) => {
			// Xử lý dữ liệu trả về ở đây
			ChildRecordDetail.value = response
		},
		onError: (error) => {
			// Xử lý lỗi ở đây
			console.error("Error fetching child record:", error)
		},
		auto: true, // Tự động fetch dữ liệu khi hàm được gọi
	})
}

// Sử dụng createListResource để lấy danh sách các trường của một Doctype
const getFieldChildTable = (doctype) => {
	return createResource({
		url: "xxx.api.childrecord.get_field_child_record",
		params: {
			doctype: doctype, // Doctype con
		},
		onSuccess: (response) => {
			ChildTableField.value = response
		},
		onError: (error) => {
			console.error(`Lỗi khi tải dữ liệu cho ${doctype}:`, error)
		},
		auto: true, // Tự động gọi API khi hàm được gọi
	})
}

async function deleteRecord(data, doctype, doctypeActive) {
	deleteChildResource(props.doctype, props.employeeId, doctype, data, doctypeActive)
}

function deleteChildResource(
	parentDoctype,
	parentName,
	childDoctypeName,
	childName,
	childDoctype
) {
	// Tạo resource cho việc xóa
	const resource = createResource({
		url: "xxx.api.childrecord.delete_child_record", // API URL
		method: "POST", // Phương thức HTTP POST
		params: {
			parent_doctype: parentDoctype,
			parent_name: parentName,
			child_table_field: childDoctypeName,
			child_name: childName,
		},
		onSuccess: (response) => {

			createTableResource(childDoctype, props.employeeId)
			createToast({
				title: __("Xoa bản ghi thành công"),
				icon: "check",
				iconClasses: "text-green-600",
			})
		},
		onError: (error) => {

			createToast({
				title: __("Error updating Employee"),
				text: __(error.messages?.[0]),
				icon: "x",
				iconClasses: "text-red-600",
			})
		},
		auto: false, // Không tự động gọi, chỉ gọi khi cần
	})
	// Gọi API xóa bản ghi
	resource.fetch()
}

// Sử dụng createResource để cập nhật bản ghi con trong bảng con của bản ghi cha
function updateChildRecord(
	parent_doctype,
	parent_name,
	child_table_field,
	child_name,
	updates,
	childDoctype
) {
	const updatesCopy = JSON.parse(JSON.stringify(updates))
	return createResource({
		url: "xxx.api.childrecord.update_child_record", // API cập nhật backend
		params: {
			parent_doctype: parent_doctype, // Doctype của bản ghi cha
			parent_name: parent_name, // Tên bản ghi cha
			child_table_field: child_table_field, // Trường bảng con trong tài liệu cha
			child_name: child_name, // Tên của bản ghi con cần cập nhật
			updates: updatesCopy, // Các dữ liệu cần cập nhật cho bản ghi con
		},
		onSuccess: (response) => {
			// Xử lý kết quả trả về ở đây

			createTableResource(childDoctype, props.employeeId)
			showModalAddChildRecord.value = false
			createToast({
				title: __("Sửa bản ghi thành công"),
				icon: "check",
				iconClasses: "text-green-600",
			})
		},
		onError: (error) => {
			// Xử lý lỗi nếu có

			createToast({
				title: __("Co loi xay ra"),
				text: __(error.messages?.[0]),
				icon: "x",
				iconClasses: "text-red-600",
			})
		},
		auto: true, // Tự động gửi yêu cầu khi hàm được gọi
	})
}

const updateMultiSelect = () => {
	emit("updateRecord")
}

const handleFileUploadSuccess = (file, fieldName) => {

	props.data[fieldName] = file.file_url // Lưu URL hoặc tên file
}

const clearFile = (fieldName) => {

	props.data[fieldName] = null // Reset giá trị về null
}
</script>

<style scoped>
:deep(.form-control.prefix select) {
	padding-left: 2rem;
}

.section {
	display: none;
}

.section:has(.settings-field) {
	display: block;
}
</style>
