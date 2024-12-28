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
				label="Create"
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
import { call, FeatherIcon, createResource, Breadcrumbs, Button } from "frappe-ui";
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

const breadcrumbs = [{ label: __("ats_institutions"), route: { name: "ats_institutions" } }];

const listdatayyy = ref([]);
const detailMode = ref(false);
const infolistyyy = reactive({});

const getcolumnsyyy = createResource({
	url: "xxx.api.doc.get_column_doctype",
	params: {
		doctype: "ATS-Institution",
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
	url: "xxx.xxx.doctype.ats_institution.api.get_yyy",
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
		url: "xxx.xxx.doctype.ats_institution.api.create_yyy",
		debounce: 500,
		params: {
			institution_name: infolistyyy.institution_name,
			location: infolistyyy.location,
			type: infolistyyy.type,
		},
		onSuccess: (data) => {
			createToast({
				title: __("Tạo thành công."),
				icon: "check",
				iconClasses: "text-green-800",
			});
			if (data.data) {
				router.push({ name: "ats_institution", params: { yyyId: data.data } });
			}
		},
		onError: (error) => {
			// Kiểm tra và hiển thị lỗi từ API
			const errorDetails = error.messages[0].details || __("Đã xảy ra lỗi không xác định.");
			createToast({
				title: __("Tạo không thành công."),
				text: errorDetails,
				icon: "alert-circle",
				iconClasses: "text-red-800",
			});
		},
	});
	createinfoyyy.fetch();
};
</script>
