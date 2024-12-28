<template>
	<Dialog
		v-model="show"
		:options="{
			size: '4xl',
		}"
	>
		<template #body>
			<div class="bg-white px-4 pb-6 pt-5 sm:px-6">
				<div class="mb-5 flex items-center justify-between">
					<div>
						<h3 class="text-2xl font-semibold leading-6 text-gray-900">
							{{ editMode ? "Sửa bản ghi" : "Tạo bản ghi mới" }}
						</h3>
					</div>
				</div>
				<div>
					<div class="grid grid-cols-1 gap-4">
						<!-- Hiển thị các Fields trong mỗi Column -->

						<div v-for="section in copyField" :key="section.label">
							<!-- Hiển thị các Columns trong mỗi Section -->
							<div
								:class="`grid gap-4 ${
									section.columns.length === 1 ? 'grid-cols-1' : 'grid-cols-2'
								}`"
							>
								<div v-for="column in section.columns" :key="section.label + column.fields.length" >
									<!-- Hiển thị các Fields trong mỗi Column -->
									<div v-for="field in column.fields" :key="field.name" class="">
										<FormControlCustom
											v-if="field.type == 'Data'"
											:type="'text'"
											size="sm"
											variant="subtle"
											:label="field.label"
											v-model="infoEmployee[field.name]"
											class="mb-3"
											:required="field.mandatory == 1 ? true : false"
										/>
										<FormControlCustom
											v-if="field.type == 'Currency'"
											:type="'text'"
											size="sm"
											variant="subtle"
											:label="field.label"
											v-model="infoEmployee[field.name]"
											class="mb-3"
											:required="field.mandatory == 1 ? true : false"
										/>
										<FormControlCustom
											v-if="field.type == 'Check'"
											:type="'checkbox'"
											size="sm"
											variant="outline"
											:label="field.label"
											v-model="infoEmployee[field.name]"
											:required="field.mandatory == 1 ? true : false"
										/>
										<FormControlCustom
											v-else-if="field.type == 'Select'"
											type="select"
											:options="field.options"
											size="sm"
											variant="subtle"
											:label="field.label"
											v-model="infoEmployee[field.name]"
											class="mb-3"
											:required="field.mandatory == 1 ? true : false"
										/>
										<FormControlCustom
											v-else-if="field.type == 'Date'"
											:type="'date'"
											size="sm"
											variant="subtle"
											:label="field.label"
											v-model="infoEmployee[field.name]"
											class="mb-3"
											:required="field.mandatory == 1 ? true : false"
										/>
										<FormControlCustom
											v-else-if="field.type == 'Float' || field.type == 'Int'"
											:type="'number'"
											size="sm"
											variant="subtle"
											:label="field.label"
											v-model="infoEmployee[field.name]"
											class="mb-3"
											:required="field.mandatory == 1 ? true : false"
										/>
										<TextEditor
											v-else-if="field.type === 'Text Editor'"
											ref="content"
											variant="outline"
											:class="'w-full'"
											:label="field.label"
											:content="infoEmployee[field.name]"
											:placeholder="getPlaceholder(field)"
											:bubbleMenu="true"
											:fixedMenu="true"
											@change="(content) => (infoEmployee[field.name] = content)"
											editor-class="!prose-sm !w-full overflow-auto !max-w-full min-h-[180px] max-h-80 py-1.5 px-2 rounded border border-gray-300 bg-white hover:border-gray-400 hover:shadow-sm focus:bg-white focus:border-gray-500 focus:shadow-sm focus:ring-0 focus-visible:ring-2 focus-visible:ring-gray-400 text-gray-800 transition-colors"
										/>
										<div v-else-if="field.type === 'Dropdown'">
											<NestedPopover>
												<template #target="{ open }">
													<Button
														:label="infoEmployee[field.name]"
														class="dropdown-button flex w-full items-center justify-between rounded border border-gray-100 bg-gray-100 px-2 py-1.5 text-base text-gray-800 placeholder-gray-500 transition-colors hover:border-gray-200 hover:bg-gray-200 focus:border-gray-500 focus:bg-white focus:shadow-sm focus:outline-none focus:ring-0 focus-visible:ring-2 focus-visible:ring-gray-400"
													>
														<div class="truncate">{{ infoEmployee[field.name] }}</div>
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
										<div class="flex gap-1" v-else-if="field.type === 'Link'">
											<Link
												class="form-control flex-1"
												:value="infoEmployee[field.name]"
												:label="field.label"
												:doctype="field.options"
												:filters="field.filters"
												@change="(v) => (infoEmployee[field.name] = v)"
												:placeholder="getPlaceholder(field)"
												:onCreate="field.create"
											/>
											<Button
												v-if="infoEmployee[field.name] && field.edit"
												class="shrink-0"
												:label="__('Edit')"
												@click="field.edit(infoEmployee[field.name])"
											>
												<template #prefix>
													<EditIcon class="h-4 w-4" />
												</template>
											</Button>
										</div>
										<FormControl
											v-else-if="['Small Text', 'Text', 'Long Text'].includes(field.type)"
											:label="field.label"
											type="textarea"
											v-model="infoEmployee[field.name]"
										/>
										<FormControl
											v-else-if="field.type == 'Time'"
											:type="'time'"
											size="sm"
											variant="subtle"
											:label="field.label"
											v-model="infoEmployee[field.name]"
											class="mb-3"
											:required="field.mandatory == 1 ? true : false"
										/>
										<div v-else-if="field.type === 'Rating'" class="flex flex-col justify-center h-full">
											<span class="text-gray-600 text-xs mb-2.5">{{ field.label }}</span>
											<StarRating
												:rating="infoEmployee[field.name]"
												:static="false"
												@update:rating="
													(rating) => (console.log(rating), (infoEmployee[field.name] = rating))
												"
											/>
										</div>

										<!-- Thêm các loại field khác nếu cần -->
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
			<div class="px-4 pb-7 pt-4 sm:px-6">
				<div class="space-y-2">
					<div class="flex flex-row-reverse gap-2">
						<Button
							:variant="'solid'"
							:label="editMode ? 'Cập nhật' : 'Tạo mới'"
							@click="editMode ? callUpdateDoc() : callInsertDoc(props.doctype)"
						/>
					</div>
				</div>
			</div>
		</template>
	</Dialog>
</template>

<script setup>
import Fields from "@/components/Fields.vue"
import { capture } from "@/telemetry"
import { Button, call, createResource, TextEditor } from "frappe-ui"
import { ref, nextTick, watch, computed, defineEmits } from "vue"
import { createToast } from "@/utils"
import { useRouter } from "vue-router"
import FormControlCustom from "../frappe-ui-custom/FormControlCustom/FormControlCustom.vue"
import StarRating from "@/components/StarRating.vue"
import NestedPopover from "@/components/NestedPopover.vue"
import DropdownItem from "@/components/DropdownItem.vue"
import Link from "@/components/Controls/Link.vue"

const props = defineProps({
	doctype: {
		type: String,
		default: "",
	},
	parentName: {
		type: String,
		default: "",
	},
	parentfield: {
		type: String,
		default: "",
	},
	parent: {
		type: String,
		default: "",
	},
	detailChildTable: {
		type: Object,
		default: null,
	},
	options: {
		type: Object,
		default: {
			redirect: true,
			detailMode: false,
			afterInsert: () => {},
		},
	},
	fields: {
		type: Array,
		default: [],
	},
})

const emit = defineEmits(["updateRecord"])

const copyField = ref({ ...props.fields })
const propsDoctype = ref({ ...props.doctype })
const infoEmployee = ref({})

// Hàm tạo dữ liệu form từ fields
function createInfoEmployee(fields) {
	const info = {}

	fields.forEach((section) => {
		section.columns.forEach((column) => {
			column.fields.forEach((field) => {
				// Nếu detailChildTable có dữ liệu, đặt giá trị mặc định từ đó, ngược lại là giá trị rỗng
				info[field.name] = props.detailChildTable ? props.detailChildTable[field.name] || "" : ""
			})
		})
	})
	return info
}

const editMode = ref(false) // Nếu có detailChildTable thì là chế độ sửa

watch(
	() => props.detailChildTable,
	(newVal) => {
		if (newVal === null) {
			editMode.value = false
		} else {
			editMode.value = true
		}
	}
)

watch(
	() => props.fields,
	(newVal) => {
		copyField.value = { ...newVal } // Cập nhật newRecord khi props thay đổi
		infoEmployee.value = createInfoEmployee(newVal)
	},
	{ immediate: true }
)

watch(
	() => props.doctype,
	(newVal) => {
		propsDoctype.value = { ...newVal } // Cập nhật newRecord khi props thay
	},
	{ immediate: true }
)

const router = useRouter()
const show = defineModel()

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

// Tạo mới bản ghi
const callUpdateDoc = () => {
	console.log(infoEmployee.value)
	emit("updateRecord", {
		infoEmployee: infoEmployee.value,
		doctype: props.detailChildTable.doctype,
		parentField: props.detailChildTable.parentfield,
	})
}

async function callInsertDoc(doctype) {
	const doc = await call("frappe.client.insert", {
		doc: {
			doctype: props.doctype,
			...infoEmployee.value,
			parenttype: props.parentName, // Tên của Doctype cha
			parent: props.parent, // Tên của bản ghi cha
			parentfield: props.parentfield, // Trường trong Doctype cha liên kết với bảng con
		},
	})
	if (doc.name) {
		capture("contact_created")
		handleContactUpdate(doc)
		createToast({
			title: __("Thêm bản ghi thành công"),
			icon: "check",
			iconClasses: "text-green-600",
		})
	} else {
		createToast({
			title: __("Co loi xay ra"),
			icon: "x",
			iconClasses: "text-red-600",
		})
	}
}

function handleContactUpdate(doc) {
	show.value = false
	props.options.afterInsert && props.options.afterInsert(doc)
}

// 2 trạng thái một sửa một, 1 tạo mới
const dialogOptions = computed(() => {
	let title = editMode.value ? "Update Record" : "Create New Record"
	let actions = [
		{
			label: editMode.value ? "Update" : "Create",
			variant: "solid",
			onClick: () => (editMode.value ? callUpdateDoc() : callInsertDoc()),
		},
	]

	return { title, size: "xl", actions }
})
</script>

<style scoped>
:deep(:has(> .dropdown-button)) {
	width: 100%;
}
</style>
