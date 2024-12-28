<template>
  <LayoutHeader>
    <template #left-header>
      <Breadcrumbs :items="breadcrumbs">
        <template #prefix="{ item }">
          <Icon :icon="item.icon" class="mr-2 h-4" />
        </template>
      </Breadcrumbs>
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
    </template>
  </LayoutHeader>
  <div class="flex h-full overflow-hidden">
    <Tabs v-model="tabIndex" :tabs="tabs">
      <template #default="{ tab }">
        <!-- Hiển thị component Activities khi tab là Activity, Comments hoặc Attachments -->
        <Activities
          ref="activities"
          doctype="xxx_yyy"
          :tabs="tabs"
          v-if="['Activity', 'Comments', 'Attachments'].includes(tab.name)"
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
            <div
              v-for="section in listdatayyy"
              :key="section.label"
              class="p-4"
            >
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
                  :doctype="'xxx_yyy'"
                  :employeeId="props.yyyId"
                  @updateRecord="() => getyyy.fetch()"
                />
              </div>
            </div>
          </FadedScrollableDiv>
        </div>
      </template>
    </Tabs>
  </div>
</template>

<script setup>
import Fields from "@/components/FieldsCustom.vue";

import LayoutHeader from "@/components/LayoutHeader.vue";
import { createToast } from "@/utils";
import Resizer from "@/components/Resizer.vue";
import EditIcon from '@/components/Icons/EditIcon.vue'
import ActivityIcon from "@/components/Icons/ActivityIcon.vue";
import CommentIcon from "@/components/Icons/CommentIcon.vue";
import AttachmentIcon from "@/components/Icons/AttachmentIcon.vue";
import DocumentIcon from "@/components/Icons/DocumentIcon.vue";
import {
  call,
  FeatherIcon,
  createResource,
  Breadcrumbs,
  Button,
  Tabs,
} from "frappe-ui";
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

const breadcrumbs = [{ label: __("yyy"), route: { name: "yyys" } }];

const listdatayyy = ref([]);
const detailMode = ref(false);
const infolistyyy = reactive({});
const datayyy = reactive({});

const getyyy = createResource({
  url: "xxx.xxx.doctype.xxx_yyy.api.get_yyy",
  params: { name: props.yyyId },
  auto: true,
  onSuccess: (data) => {
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
    doctype: "xxx_yyy",
  },
  auto: true,
  onSuccess: async (data) => {
    listdatayyy.value = data;
  },
});

const tableFields = {
  xxx_yyy_child_table: ["first_name", "last_name"],
};

const tableData = reactive({
  xxx_yyy_child_table: { columns: [], rows: [] },
});

const dynamicTables = ["xxx_yyy_child_table"];

const updateInfo = () => {
  const updateinfoyyy = createResource({
    url: "xxx.xxx.doctype.xxx_yyy.api.update_yyy",
    debounce: 500,
    params: {
      yyyId: props.yyyId,
      ho_va_ten: infolistyyy.ho_va_ten,
      kieu_check: infolistyyy.kieu_check,
      kieu_date: infolistyyy.kieu_date,
      kieu_datetime: infolistyyy.kieu_datetime,
      kieu_float: infolistyyy.kieu_float,
      kieu_int: infolistyyy.kieu_int,
      kieu_rating: infolistyyy.kieu_rating,
      kieu_select: infolistyyy.kieu_select,
      kieu_small_text: infolistyyy.kieu_small_text,
      kieu_text_editor:infolistyyy.kieu_text_editor,
      kieu_text: infolistyyy.kieu_text,
      kieu_link:infolistyyy.kieu_link,
    },
    onSuccess: (data) => {
      createToast({
        title: __("Cập nhật yyy thành công."),
        icon: "check",
        iconClasses: "text-green-800",
      });
      getyyy.fetch();
    },
    onError: (error) => {},
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
  return [...activitiesTabs.value].filter((tab) =>
    tab.condition ? tab.condition() : true
  );
});

const { tabIndex } = useActiveTabManager(tabs, "Details");

const fieldsLayout = createResource({
  url: "xxx.api.doc.get_sidebar_fields",
  cache: ["fieldsLayout", props.yyyId],
  params: { doctype: "xxx_yyy", name: props.yyyId },
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
      doctype: "xxx_yyy",
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

watch(
  () => route.params.id, // Theo dõi sự thay đổi của route params
  (newId, oldId) => {
    if (newId !== oldId) {
      fieldsLayout.fetch();
    }
  },
  { immediate: true } // Gọi ngay khi component được khởi tạo
);
</script>
