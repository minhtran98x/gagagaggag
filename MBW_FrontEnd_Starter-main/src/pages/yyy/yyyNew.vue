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
        @click="() => createInfo()"
      >
        Tạo mới
      </Button>
      <!-- <ActionDoctype
        doctype="xxx_yyy"
        :doc="infolistyyy"
        :isNew="true"
        :onSave="createInfo"
      ></ActionDoctype> -->
    </template>
  </LayoutHeader>
  <div class="flex flex-col gap-4 m-5 h-full">
    <div v-for="section in listdatayyy" :key="section.label">
      <h3 class="font-semibold text-lg mt-6 mb-4">
        {{ section.label }}
      </h3>
      <Fields
        v-if="section.columns"
        :sections="section.columns"
        :data="infolistyyy"
        :isCreateModal="true"
      />
    </div>
  </div>
</template>

<script setup>
import Fields from "@/components/FieldsCustom.vue";
import LayoutHeader from "@/components/LayoutHeader.vue";
import ActionDoctype from "@/components/ActionDoctype.vue";

import { createToast } from "@/utils";
import {
  call,
  FeatherIcon,
  createResource,
  Breadcrumbs,
  Button,
} from "frappe-ui";
import { ref, nextTick, watch, computed, h, reactive, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";

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

const route = useRoute();
const router = useRouter();

const breadcrumbs = [{ label: __("yyy"), route: { name: "yyys" } }];

const listdatayyy = ref([]);
const detailMode = ref(false);
const infolistyyy = reactive({});

const getcolumnsyyy = createResource({
  url: "xxx.api.doc.get_column_doctype",
  params: {
    doctype: "xxx_yyy",
  },
  auto: true,
  onSuccess: async (data) => {
    listdatayyy.value = data;
    for (const section of data) {
      for (const column of section.columns) {
        for (const field of column.fields) {
          infolistyyy[field.name] = field.default || "";
        }
      }
    }

    if (route.query.amended_from) {
      await getDocAmend.fetch();
    }
  },
});

const getDocAmend = createResource({
  url: "xxx.xxx.doctype.xxx_yyy.api.get_yyy",
  params: {
    name: route.query.amended_from,
  },
  onSuccess: async (data) => {
    const keys = Object.keys(data);
    for (let key of keys) {
      infolistyyy[key] = data[key];
    }
    infolistyyy["amended_from"] = route.query.amended_from;
  },
});

const createInfo = () => {
  const createinfoyyy = createResource({
    url: "xxx.xxx.doctype.xxx_yyy.api.create_yyy",
    debounce: 500,
    params: {
      ho_va_ten: infolistyyy.ho_va_ten,
      kieu_check: infolistyyy.kieu_check,
      kieu_date: infolistyyy.kieu_date,
      kieu_datetime: infolistyyy.kieu_datetime,
      kieu_float: infolistyyy.kieu_float,
      kieu_int: infolistyyy.kieu_int,
      kieu_rating: infolistyyy.kieu_rating,
      kieu_select: infolistyyy.kieu_select,
      kieu_small_text: infolistyyy.kieu_small_text,
      kieu_text: infolistyyy.kieu_text,
      kieu_link: infolistyyy.kieu_link,
      kieu_text_editor: infolistyyy.kieu_text_editor,
      kieu_attach: infolistyyy.kieu_attach,
    },
    onSuccess: (data) => {
      createToast({
        title: __("Tạo yyy thành công."),
        icon: "check",
        iconClasses: "text-green-800",
      });
      if (data.data) {
        router.push({ name: "yyy", params: { yyyId: data.data } });
      }
    },
    onError: (error) => {
      console.log(error);
    },
  });
  createinfoyyy.fetch();
};
</script>
