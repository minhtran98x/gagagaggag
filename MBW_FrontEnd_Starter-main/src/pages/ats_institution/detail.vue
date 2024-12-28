<template>
	<LayoutHeader>
		<template #left-header>
			<Breadcrumbs :items="breadcrumbs">
				<template #prefix="{ item }">
					<Icon :icon="item.icon" class="mr-2 h-4" />
				</template>
			</Breadcrumbs>

			<!-- <StatusDoctype
          :configDoc="configDoc"
          :doc="infolistyyy"
          :isDirty="isDirty"
        ></StatusDoctype> -->
		</template>
		<template #right-header>
			<Button
				:variant="'solid'"
				:ref_for="true"
				theme="gray"
				size="sm"
				label="Cập nhật"
				:loading="false"
				:loadingText="null"
				:disabled="false"
				:link="null"
				@click="() => updateInfo()"
			>
				Cập nhật
			</Button>
			<!-- <ActionDoctype
          doctype="xxx_yyy"
          :doc="infolistyyy"
          deleteRedirect="/yyys"
          createRedirect="/yyyNew"
          :onSave="updateInfo"
          :reloadDoc="() => getyyy.fetch()"
          v-model:configDoc="configDoc"
          v-model:isDirty="isDirty"
        ></ActionDoctype> -->
		</template>
	</LayoutHeader>
	<div class="flex h-full overflow-hidden">
		<Tabs v-model="tabIndex" :tabs="tabs">
			<template #default="{ tab }">
				<!-- Hiển thị component Activities khi tab là Activity, Comments hoặc Attachments -->
				<Activities
					ref="activities"
					doctype="ATS-Institution"
					:tabs="tabs"
					v-if="['Activity', 'Comments', 'Attachments'].includes(tab.name) && getyyy.data"
					v-model:reload="reload"
					v-model:tabIndex="tabIndex"
					v-model="getyyy"
				/>

				<div v-else>
					<div class="p-4">
						<h3 class="font-semibold text-lg mt-2 mb-2">Details</h3>
					</div>
					<FadedScrollableDiv
						:maskHeight="20"
						class="flex flex-col flex-1 max-h-[80vh] overflow-y-auto"
					>
						<!-- Hiển thị các section cho các tab khác -->
						<div v-for="section in listdatayyy" :key="section.label" class="p-4">
							<h3 class="font-semibold text-lg mt-2 mb-2">
								{{ section.label }}
							</h3>
							<div>
								<Fields
									v-if="section.columns"
									:sections="section.columns"
									:data="infolistyyy"
									:tableFields="tableFields"
									:tableData="tableData"
									:dynamicTables="dynamicTables"
									:doctype="'ATS-Institution'"
									:employeeId="props.yyyId"
									@updateRecord="() => getyyy.fetch()"
								/>
							</div>
						</div>
					</FadedScrollableDiv>
				</div>
			</template>
		</Tabs>

		<Resizer class="flex flex-col border-l" side="right">
			<div
				class="flex h-10.5 cursor-copy items-center border-b px-5 py-2.5 text-lg font-medium"
				@click="copyToClipboard(infolistyyy?.name)"
			>
				{{ __(infolistyyy?.institution_name) }}
			</div>

			<div
				v-if="fieldsLayout.data"
				class="flex flex-1 flex-col justify-between overflow-hidden"
			>
				<div class="flex flex-col overflow-y-auto">
					<div
						v-for="(section, i) in fieldsLayout.data"
						:key="section.label"
						class="section flex flex-col p-3"
						:class="{ 'border-b': i !== fieldsLayout.data.length - 1 }"
					>
						<Section :is-opened="section.opened" :label="section.label">
							<template #actions>
								<Button
									variant="ghost"
									class="w-7"
									@click="showSidePanelModal = true"
								>
									<EditIcon class="h-4 w-4" />
								</Button>
							</template>
							<SectionFields
								v-if="section.fields"
								:fields="section.fields"
								:isLastSection="i == fieldsLayout.data.length - 1"
								v-model="datayyy"
								@update="updateField"
							/>
						</Section>
					</div>
				</div>
			</div>
		</Resizer>
	</div>

	<SidePanelModal
		v-if="showSidePanelModal"
		v-model="showSidePanelModal"
		doctype="ATS-Institution"
		@reload="() => fieldsLayout.reload()"
	/>
</template>

<script setup>
import ActionDoctype from "@/components/ActionDoctype.vue";
import StatusDoctype from "@/components/StatusDoctype.vue";
import Fields from "@/components/FieldsCustom.vue";
import SidePanelModal from "@/components/Settings/SidePanelModal.vue";
import LayoutHeader from "@/components/LayoutHeader.vue";
import { createToast } from "@/utils";
import Resizer from "@/components/Resizer.vue";
import EditIcon from "@/components/Icons/EditIcon.vue";
import ActivityIcon from "@/components/Icons/ActivityIcon.vue";
import CommentIcon from "@/components/Icons/CommentIcon.vue";
import AttachmentIcon from "@/components/Icons/AttachmentIcon.vue";
import DocumentIcon from "@/components/Icons/DocumentIcon.vue";
import { call, FeatherIcon, createResource, Breadcrumbs, Button, Tabs } from "frappe-ui";
import { ref, nextTick, watch, computed, h, reactive, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useActiveTabManager } from "@/composables/useActiveTabManager";
import FadedScrollableDiv from "@/components/FadedScrollableDiv.vue";
import Activities from "@/components/Activities/Activities.vue";
import Section from "@/components/Section.vue";
import SectionFields from "@/components/SectionFields.vue";

const props = defineProps({
	options: {
		type: Object,
		default: {
			redirect: true,
			detailMode: false,
			afterInsert: () => {},
		},
	},
	yyyId: {
		type: String,
		required: true,
	},
});

const router = useRouter();
const route = useRoute();

const breadcrumbs = [{ label: __("ats_institutions"), route: { name: "ats_institutions" } }];
const showSidePanelModal = ref(false);
const listdatayyy = ref([]);
const detailMode = ref(false);
const listPermission = ref({});
const infolistyyy = reactive({});
const datayyy = reactive({});

// actions and status of doctype
const isDirty = ref(false);
const configDoc = ref();

const getyyy = createResource({
	url: "xxx.xxx.doctype.ats_institution.api.get_yyy",
	params: { name: props.yyyId },
	auto: true,
	onSuccess: (data) => {
		isDirty.value = false;

		for (const key in data) {
			if (data.hasOwnProperty(key)) {
				infolistyyy[key] = data[key];
				datayyy[key] = data[key];
			}
		}
	},
});

const getcolumnsyyy = createResource({
	url: "xxx.api.doc.get_column_doctype",
	params: {
		doctype: "ATS-Institution",
	},
	auto: true,
	onSuccess: async (data) => {
		listdatayyy.value = data;
	},
});

const tableFields = {
	xxx_yyy_child_table: [],
};

const tableData = reactive({
	xxx_yyy_child_table: { columns: [], rows: [] },
});

const dynamicTables = [];

const updateInfo = () => {
	const updateinfoyyy = createResource({
		url: "xxx.xxx.doctype.ats_institution.api.update_yyy",
		debounce: 500,
		params: {
			yyyId: props.yyyId,
			institution_name: infolistyyy.institution_name,
			location: infolistyyy.location,
			type: infolistyyy.type,
		},
		onSuccess: (data) => {
			createToast({
				title: __("Cập nhật yyy thành công."),
				icon: "check",
				iconClasses: "text-green-800",
			});
			getyyy.reload();
		},
		onError: (err) => {
			createToast({
				title: __("An error occurred."),
				text: err.messages[0].details,
				icon: "x",
				iconClasses: "text-red-600",
			});
		},
	});
	updateinfoyyy.fetch();
};

// KHoi taoj cac tab
const activitiesTabs = computed(() => {
	let tabOptions = [
		{
			name: "Details",
			label: __("Details"),
			icon: DocumentIcon,
		},
		{
			name: "Activity",
			label: __("Activity"),
			icon: ActivityIcon,
		},
		{
			name: "Comments",
			label: __("Comments"),
			icon: CommentIcon,
		},
		{
			name: "Attachments",
			label: __("Attachments"),
			icon: AttachmentIcon,
		},
	];
	return tabOptions.filter((tab) => (tab.condition ? tab.condition() : true));
});

// Kết hợp activitiesTabs và additionalTabs thành một mảng duy nhất
const tabs = computed(() => {
	// Kết hợp cả các tab chính và bổ sung
	return [...activitiesTabs.value].filter((tab) => (tab.condition ? tab.condition() : true));
});

const { tabIndex } = useActiveTabManager(tabs, "Details");

const fieldsLayout = createResource({
	url: "xxx.api.doc.get_sidebar_fields",
	cache: ["fieldsLayout", props.yyyId],
	params: { doctype: "ATS-Institution", name: props.yyyId },
	auto: true,
});

function validateRequired(fieldname, value) {
	let meta = getyyy.data.fields_meta || {};
	if (meta[fieldname]?.reqd && !value) {
		createToast({
			title: __("Error Updating Employee"),
			text: __("{0} is a required field", [meta[fieldname].label]),
			icon: "x",
			iconClasses: "text-red-600",
		});
		return true;
	}
	return false;
}

function updatexxx(fieldname, value, callback) {
	value = Array.isArray(fieldname) ? "" : value;

	if (!Array.isArray(fieldname) && validateRequired(fieldname, value)) return;

	createResource({
		url: "frappe.client.set_value",
		params: {
			doctype: "ATS-Institution",
			name: props.yyyId,
			fieldname,
			value,
		},
		auto: true,
		onSuccess: () => {
			getyyy.reload();

			createToast({
				title: __("Record updated"),
				icon: "check",
				iconClasses: "text-green-600",
			});
			callback?.();
		},
		onError: (err) => {
			createToast({
				title: __("Error updating Record"),
				text: __(err.messages?.[0]),
				icon: "x",
				iconClasses: "text-red-600",
			});
		},
	});
}

function updateField(name, value, callback) {
	updatexxx(name, value, () => {
		getyyy.data[name] = value;
		callback?.();
	});
}
// onMounted(async () => {
// 	// await getListPermission("xxx_yyy")
// 	await fetchPermissions("xxx_yyy");
// });
// const fetchPermissions = async (doctype) => {
// 	const resource = await createResource({
// 		url: "xxx.api.permission.check_user_permissions", // Thay "your_app" bằng tên ứng dụng của bạn
// 		params: { doctype },
// 		auto: true,
// 		onSuccess(data) {
// 			console.log(data);
// 			listPermission.value = data?.permissions;
// 		},
// 	});
// 	resource.fetch();
// };
watch(
	() => route.params.id, // Theo dõi sự thay đổi của route params
	(newId, oldId) => {
		if (newId !== oldId) {
			fieldsLayout.fetch();
		}
	},
	{ immediate: true }, // Gọi ngay khi component được khởi tạo
);
</script>
