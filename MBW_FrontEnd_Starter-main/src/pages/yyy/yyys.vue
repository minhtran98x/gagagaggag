<template>
  <LayoutHeader>
    <template #left-header>
      <Breadcrumbs :items="breadcrumbs" />
    </template>
    <template #right-header>
      <Autocomplete
        :value="valueType.label"
        :options="[
          { label: 'Modal View', value: '1' },
          { label: 'Page View', value: '2' },
        ]"
        :size="'sm'"
        @change="(e) => addTypeView(e)"
        :placeholder="__('Type View')"
      >
      </Autocomplete>

      <!-- Button tạo mới dành cho type page -->
      <RouterLink
        :to="{
          name: 'yyyNew',
        }"
      >
        <Button
          
          label="Create"
          theme="gray"
          variant="solid"
        >
          <template #prefix>
            <FeatherIcon name="plus" class="h-4" />
          </template>
        </Button>
      </RouterLink>

      <!-- Button tạo mới dành cho type modal -->
      <Button
        v-if="valueType.value === '1' && listPermission?.create"
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
    doctype="xxx_yyy"
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
  />
  <div
    v-else-if="yyylist.data && valueType.value === '2'"
    class="flex h-full items-center justify-center"
  >
    <div
      class="flex flex-col items-center gap-3 text-xl font-medium text-gray-500"
    >
      <EmailIcon class="h-10 w-10" />
      <span>{{ __("No yyys Found") }}</span>
    </div>
  </div>

  <yyyModal
    v-if="valueType.value === '1'"
    v-model="showinfoyyymodal"
    :list_field_value="list_field_value"
    :editMode="editMode"
    :listPermission="listPermission"
    v-model:quickEntry="showQuickEntryModal"
  ></yyyModal>

  <QuickEntryModal
    v-if="showQuickEntryModal && valueType.value == '1'"
    v-model="showQuickEntryModal"
    doctype="xxx_yyy"
  />
</template>

<script setup>
import EmailIcon from "@/components/Icons/EmailIcon.vue";
import Autocomplete from "@/components/frappe-ui/Autocomplete.vue";
import LayoutHeader from "@/components/LayoutHeader.vue";
import ViewControls from "@/components/ViewControls.vue";
import QuickEntryModal from "@/components/Modals/QuickEntryModal.vue";
import yyyModal from "@/components/Modals/yyyModal.vue";
import yyyListView from "@/components/ListViews/yyyListView.vue";
// import { useUserPermissionStore } from '@/stores/userPermissionStore.js'
import { Breadcrumbs, Button, createResource } from "frappe-ui";
import { ref, computed, onMounted } from "vue";

const breadcrumbs = [{ label: __("yyys"), route: { name: "yyys" } }];

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

const defaultValue = localStorage.getItem("typeView")
  ? JSON.parse(localStorage.getItem("typeView"))
  : { label: "Modal View", value: "1" };

const valueType = ref(defaultValue);

function addTypeView(c) {
  if (!c || c.value === valueType.value) return;
  valueType.value = c;

  // Chỉ lưu giá trị khi chọn 'Page View'
  if (c.label === "Page View") {
    localStorage.setItem("typeView", JSON.stringify(c));
  }
}

onMounted(async () => {
  // await getListPermission("xxx_yyy")

  const savedValue = localStorage.getItem("typeView");
  if (savedValue) {
    valueType.value = JSON.parse(savedValue);
  }
  await fetchPermissions("xxx_yyy");
});

const showinfoyyymodal = ref(false);
const editMode = ref(false);
const showQuickEntryModal = ref(false);
const list_field_value = ref({
  name: "",
  ho_va_ten: "",
  kieu_check: "",
  kieu_datetime: "",
});

async function showyyy(name) {
  let t = rows.value?.find((row) => row.name === name);
  list_field_value.value = {
    name: t.name,
    ho_va_ten: t.ho_va_ten,
    kieu_check: t.kieu_check,
    kieu_datetime: t.kieu_datetime,
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
</script>
