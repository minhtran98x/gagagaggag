<template>
	<LayoutHeader>
		<template #left-header>
			<Breadcrumbs :items="breadcrumbs" />
		</template>
		<template #right-header>
			<!-- <Autocomplete
				:value="valueType.label"
				:options="[
					{ label: 'Modal View', value: '1' },
					{ label: 'Page View', value: '2' },
				]"
				:size="'sm'"
				@change="(e) => addTypeView(e)"
				:placeholder="__('Type View')"
			>
			</Autocomplete> -->

			<!-- Button tạo mới dành cho type page -->
			<!-- <div v-if="valueType.value === '2' && listPermission.create">
				<RouterLink
					:to="{
						name: 'atsInstitutionNew',
					}"
				>
					<Button label="Create" theme="gray" variant="solid">
						<template #prefix>
							<FeatherIcon name="plus" class="h-4" />
						</template>
					</Button>
				</RouterLink>
			</div> -->

			<Button
				v-if="valueType.value === '1'"
				variant="solid"
				label="Create"
				@click="handleCreateClick"
			>
				<template #prefix><FeatherIcon name="plus" class="h-4" /></template>
			</Button>
		</template>
	</LayoutHeader>
	<ViewControls
		ref="viewControls"
		v-model="yyylist"
		v-model:loadMore="loadMore"
		v-model:resizeColumn="triggerResize"
		v-model:updatedPageCount="updatedPageCount"
		doctype="ATS_Company"
	/>
	<yyyListView
		ref="yyysListView"
		v-if="yyylist.data && rows.length"
		v-model="yyylist.data.page_length_count"
		v-model:list="yyylist"
		:rows="rows"
		:columns="yyylist.data.columns"
		:options="{
			showTooltip: false,
			resizeColumn: true,
			rowCount: yyylist.data.row_count,
			totalCount: yyylist.data.total_count,
		}"
		:valueType="valueType.value"
		@showyyy="showyyy"
		@loadMore="() => loadMore++"
		@columnWidthUpdated="() => triggerResize++"
		@updatePageCount="(count) => (updatedPageCount = count)"
		@showTask="showTask"
		@applyFilter="(data) => viewControls.applyFilter(data)"
		@deleteRecord="yyylist.reload()"
	/>
	<div
		v-else-if="yyylist.data && valueType.value === '2'"
		class="flex h-full items-center justify-center"
	>
		<div class="flex flex-col items-center gap-3 text-xl font-medium text-gray-500">
			<EmailIcon class="h-10 w-10" />
			<span>{{ __("No data Found") }}</span>
		</div>
	</div>

	<AtsCompanyModal
		v-if="valueType.value === '1'"
		v-model="showinfoyyymodal"
		:list_field_value="list_field_value"
		:editMode="editMode"
		:listPermission="listPermission"
		v-model:quickEntry="showQuickEntryModal"
		@updateList="yyylist.reload()"
	></AtsCompanyModal>

	<QuickEntryModal v-model="showQuickEntryModal" doctype="ATS_Company" />
</template>

<script setup>
import EmailIcon from "@/components/Icons/EmailIcon.vue";
import Autocomplete from "@/components/frappe-ui/Autocomplete.vue";
import LayoutHeader from "@/components/LayoutHeader.vue";
import ViewControls from "@/components/ViewControls.vue";
import QuickEntryModal from "@/components/Modals/QuickEntryModal.vue";
import AtsCompanyModal from "@/components/Modals/atsCompanyModal.vue";
import yyyListView from "@/components/ListViews/ATSCompanyListView.vue";
// import { useUserPermissionStore } from '@/stores/userPermissionStore.js'
import { Breadcrumbs, Button, createResource } from "frappe-ui";
import { ref, computed, onMounted } from "vue";

const breadcrumbs = [{ label: __("Ats Companies"), route: { name: "ats_companies" } }];

const yyysListView = ref(null);
const yyylist = ref({});
const loadMore = ref(1);
const triggerResize = ref(1);
const updatedPageCount = ref(20);
const viewControls = ref(null);
const listPermission = ref({});
// const { getListPermission,userPermission } = useUserPermissionStore()

const rows = computed(() => {
	if (!yyylist.value?.data?.data) return [];
	return yyylist.value?.data.data;
});

// const defaultValue = localStorage.getItem("typeView")
// 	? JSON.parse(localStorage.getItem("typeView"))
// 	: { label: "Modal View", value: "1" };

const defaultValue = { label: "Modal View", value: "1" };

const valueType = ref(defaultValue);

function addTypeView(c) {
	if (!c || c.value === valueType.value) return;
	valueType.value = c;

	// Chỉ lưu giá trị khi chọn 'Page View'
	if (c.label === "Page View") {
		localStorage.setItem("typeView", JSON.stringify(c));
	}
	if (c.label === "Modal View") {
		localStorage.setItem("typeView", JSON.stringify(c));
	}
}

onMounted(async () => {
	// await getListPermission("ATS-Institution");

	const savedValue = localStorage.getItem("typeView");
	if (savedValue) {
		valueType.value = JSON.parse(savedValue);
	}
	// await fetchPermissions("ATS_Company");
});

const showinfoyyymodal = ref(false);
const editMode = ref(false);
const showQuickEntryModal = ref(false);
const list_field_value = ref({
	name: "",
	company_id: "",
	company_name: "",
	company_address: "",
	company_head: "",
	cat_order: "",
	cat_status: true,
	cat_color: "",
	cat_icon: "",
});

async function showyyy(name) {
	let t = rows.value?.find((row) => row.name === name);
	list_field_value.value = {
		name: t.name,
		company_id: t.company_id,
		company_name: t.company_name,
		company_address: t.company_address,
		company_head: t.company_head,
		cat_order: t.cat_order,
		cat_status: t.cat_status,
		cat_color: t.cat_color,
		cat_icon: t.cat_icon,
	};
	editMode.value = true;
	showinfoyyymodal.value = true;
}

const handleCreateClick = () => {
	showinfoyyymodal.value = true;
	editMode.value = false;
};

const fetchPermissions = async (doctype) => {
	const resource = await createResource({
		url: "xxx.api.permission.check_user_permissions", // Thay "your_app" bằng tên ứng dụng của bạn
		params: { doctype },
		auto: true,
		onSuccess(data) {
			listPermission.value = data?.permissions;
		},
	});
	resource.fetch();
};

const flattenTree = (data, parentKey = null, level = 0) => {
  const result = [];
  data.forEach((node) => {
    if (node.parent_ats_unit === parentKey) {
      result.push({
        ...node,
        level, // Thêm thông tin cấp bậc
      });
      // Gọi đệ quy để xử lý các node con
      result.push(...flattenTree(data, node.name, level + 1));
    }
  });
  return result;
};

const buildTree = (data, parentKey = null) => {
  return data
    .filter((item) => item.parent_ats_unit === parentKey)
    .map((item) => ({
      ...item,
      children: buildTree(data, item.name), // Đệ quy để tìm các con
      collapsed: true, // Đặt trạng thái collapsed mặc định
    }));
};

const test = createResource({
	url: "xxx.api.ats_unit.get_tree_data",
	params: { doctype: "ATS_Unit" },
	auto: true,
	onSuccess(data) {
		console.log(flattenTree(data));
		const flattenData = flattenTree(data);
		const groupedData = buildTree(flattenData);
		console.log(groupedData);

	},
});
</script>
