<template>
	<ListView
		:class="$attrs.class"
		:columns="columns"
		:rows="rows"
		:options="{
			// ...(props.valueType === '1'
			// 	? { onRowClick: (row) => emit('showyyy', row.name) }
			// 	: {
			// 			getRowRoute: (row) => ({
			// 				name: 'ats_institution',
			// 				params: { yyyId: row.name },
			// 			}),
			// 		}),
			selectable: options.selectable,
			showTooltip: options.showTooltip,
			resizeColumn: options.resizeColumn,
		}"
		row-key="name"
	>
		<ListHeader class="sm:mx-5 mx-3" @columnWidthUpdated="emit('columnWidthUpdated')">
			<ListHeaderItem
				v-for="column in columns"
				:key="column.key"
				:item="column"
				@columnWidthUpdated="emit('columnWidthUpdated', column)"
			>
				<Button
					v-if="column.key == '_liked_by'"
					variant="ghosted"
					class="!h-4"
					@click="() => emit('applyLikeFilter')"
				>
					<HeartIcon class="h-4 w-4" />
				</Button>
			</ListHeaderItem>
		</ListHeader>

		<ListRows :rows="rows" v-slot="{ idx, column, item, row }" class="relative">
			<div v-if="column.key === 'location'" class="cursor-pointer">
				<Tooltip :text="item">
					<div class="flex items-center gap-2 truncate text-base">
						<div
							v-if="item"
							class="truncate"
							@click="
								(event) =>
									emit('applyFilter', {
										event,
										idx,
										column,
										item,
										firstColumn: columns[0],
									})
							"
						>
							{{ item }}
						</div>
					</div>
				</Tooltip>
			</div>
			<div v-else-if="column.key === 'training_type'" class="cursor-pointer">
				<Tooltip :text="item">
					<div class="flex items-center gap-2 truncate text-base">
						<div
							v-if="item"
							class="truncate"
							@click="
								(event) =>
									emit('applyFilter', {
										event,
										idx,
										column,
										item,
										firstColumn: columns[0],
									})
							"
						>
							{{ item }}
						</div>
					</div>
				</Tooltip>
			</div>
			<div v-else-if="column.key === 'institution_name'">
				<div class="flex items-center gap-2 truncate text-base cursor-pointer">
					<div
						v-if="item"
						class="truncate"
						@click="(event) => emit('showyyy', row.name)"
					>
						{{ item }}
					</div>
				</div>
			</div>
			<ListRowItem v-else :item="item" class="">
				<template #prefix> </template>
				<template #default="{ label }">
					<div
						class="truncate text-base"
						@dblclick="
							(event) => {
								// Hủy bỏ sự kiện click nếu dblclick xảy ra
								console.log('Double click');
								// Thực hiện logic cho dblclick ở đây
							}
						"
					>
						{{ label }}
					</div>
				</template>
			</ListRowItem>
		</ListRows>
		<ListSelectBanner>
			<template #actions="{ selections, unselectAll }">
				<Dropdown :options="listBulkActionsRef.bulkActions(selections, unselectAll)">
					<Button icon="more-horizontal" variant="ghost" />
				</Dropdown>
			</template>
		</ListSelectBanner>
	</ListView>

	<ListFooter
		v-if="pageLengthCount"
		class="border-t sm:px-5 px-3 py-2"
		v-model="pageLengthCount"
		:options="{
			rowCount: options.rowCount,
			totalCount: options.totalCount,
		}"
		@loadMore="emit('loadMore')"
	/>
	<ListBulkActions
		ref="listBulkActionsRef"
		v-model="list"
		doctype="ATS-Institution"
		:options="{
			hideAssign: true,
			hideEdit: true,
		}"
	/>
	<ConfirmModal
		v-model="showConfirmModal"
		@confirm="() => deleteRecord(fieldStore.childTableField)"
	>
		<template #title>
			<div class="text-lg font-semibold flex justify-center">
				{{ __("Xác nhận xóa") }}
			</div>
		</template>
		<template #content>
			<span class="flex justify-center">
				{{ __("Bạn có chắc chắn muốn xóa bản ghi này không?") }}
			</span>
		</template>
	</ConfirmModal>
</template>

<script setup>
import HeartIcon from "@/components/Icons/HeartIcon.vue";
import MoneyIcon from "@/components/Icons/MoneyIcon.vue";
import IndicatorIcon from "@/components/Icons/IndicatorIcon.vue";
import PhoneIcon from "@/components/Icons/PhoneIcon.vue";
import MultipleAvatar from "@/components/MultipleAvatar.vue";
import CalendarIcon from "@/components/Icons/CalendarIcon.vue";
import EmailIcon from "@/components/Icons/EmailIcon.vue";
import EmailAtIcon from "@/components/Icons/EmailAtIcon.vue";
import Email2Icon from "@/components/Icons/Email2Icon.vue";
import ListBulkActions from "@/components/ListBulkActions.vue";
import ListRows from "@/components/ListViews/ListRows.vue";
import { dateFormat } from "@/utils";
import {
	Avatar,
	ListView,
	ListHeader,
	ListHeaderItem,
	ListSelectBanner,
	ListRowItem,
	ListFooter,
	Dropdown,
	Tooltip,
	Badge,
	call,
	createResource,
} from "frappe-ui";
import { sessionStore } from "@/stores/session";
import { ref, computed, watch, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useFieldStore } from "../../stores/activeRecord";
import { createToast } from "@/utils";
import ConfirmModal from "../Modals/ConfirmModal.vue";

const fieldStore = useFieldStore();
const showConfirmModal = ref(false);

watch(
	() => fieldStore.timestamp,
	() => {
		console.log("Fields updated");
		if (fieldStore.actionType === "edit") {
			emit("showyyy", fieldStore.childTableField);
		} else if (fieldStore.actionType === "delete") {
			showConfirmModal.value = true;
		}
	},
);

const props = defineProps({
	rows: {
		type: Array,
		required: true,
	},
	columns: {
		type: Array,
		required: true,
	},
	valueType: {
		type: String,
	},
	options: {
		type: Object,
		default: () => ({
			selectable: true,
			showTooltip: true,
			resizeColumn: false,
			totalCount: 0,
			rowCount: 0,
		}),
	},
});

const emit = defineEmits([
	"loadMore",
	"updatePageCount",
	"columnWidthUpdated",
	"showyyy",
	"applyFilter",
	"applyLikeFilter",
	"likeDoc",
	"deleteRecord",
]);

const route = useRoute();

const pageLengthCount = defineModel();
const list = defineModel("list");

const isLikeFilterApplied = computed(() => {
	return list.value.params?.filters?._liked_by ? true : false;
});

const { user } = sessionStore();

function formattedDateTooltip(dateStr) {
	const [year, month, day] = dateStr.split("-");
	return `${day}/${month}/${year}`;
}
function isLiked(item) {
	if (item) {
		let likedByMe = JSON.parse(item);
		return likedByMe.includes(user);
	}
}
watch(pageLengthCount, (val, old_value) => {
	if (val === old_value) return;
	emit("updatePageCount", val);
});

const listBulkActionsRef = ref(null);

defineExpose({
	customListActions: computed(() => listBulkActionsRef.value?.customListActions),
});

function deleteRecord(name) {
	createResource({
		url: "frappe.client.delete",
		params: {
			doctype: "ATS-Institution",
			name: name,
		},
		auto: true,
		onSuccess: () => {
			emit("deleteRecord");
			createToast({
				title: __("Xóa thành công"),
				icon: "check",
				iconClasses: "text-green-600",
			});
		},
		onError: (err) => {
			createToast({
				title: __("Có lỗi xảy ra "),
				text: __(err.messages?.[0]),
				icon: "x",
				iconClasses: "text-red-600",
			});
		},
	});
}
</script>
