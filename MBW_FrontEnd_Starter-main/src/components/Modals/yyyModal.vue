<template>
	<Dialog v-model="show" :options="dialogOptions">
		<template #body>
			<div class="bg-white px-4 pb-6 pt-5 sm:px-6">
				<div class="mb-5 flex items-center justify-between">
					<div>
						<h3 class="text-2xl font-semibold leading-6 text-gray-900">
							{{ __(dialogOptions.title) || __("Untitled") }}
						</h3>
					</div>
					<div class="flex items-center gap-1">
						<Button
							v-if="isManager() || detailMode"
							variant="ghost"
							class="w-7"
							@click="detailMode ? (detailMode = false) : openQuickEntryModal()"
						>
							<EditIcon class="h-4 w-4" />
						</Button>
						<Button variant="ghost" class="w-7" @click="show = false">
							<FeatherIcon name="x" class="h-4 w-4" />
						</Button>
					</div>
				</div>
				<div>
					<div v-if="detailMode" class="flex flex-col gap-3.5">
						<div
							class="flex h-7 items-center gap-2 text-base text-gray-800"
							v-for="field in fields"
							:key="field.name"
						>
							<div class="grid w-7 place-content-center">
								<component :is="field.icon" />
							</div>
							<div>{{ field.value }}</div>
						</div>
					</div>
					<Fields
						v-else-if="filteredSections"
						:sections="filteredSections"
						:data="_yyy"
					/>
				</div>
			</div>
			<div v-if="!detailMode" class="px-4 pb-7 pt-4 sm:px-6">
				<div v-if="props.listPermission?.create || props.listPermission.write" class="space-y-2">
					<Button
						class="w-full"
						v-for="action in dialogOptions.actions"
						:key="action.label"
						v-bind="action"
						:label="__(action.label)"
						:loading="loading"
					/>
				</div>
			</div>
		</template>
	</Dialog>
</template>

<script setup>
import Fields from "@/components/FieldsCustom.vue";

import EditIcon from "@/components/Icons/EditIcon.vue";
import MoneyIcon from "@/components/Icons/MoneyIcon.vue";
import WebsiteIcon from "@/components/Icons/WebsiteIcon.vue";
import OrganizationsIcon from "@/components/Icons/OrganizationsIcon.vue";
import TerritoryIcon from "@/components/Icons/TerritoryIcon.vue";
import { usersStore } from "@/stores/users";
import { formatNumberIntoCurrency } from "@/utils";
import { capture } from "@/telemetry";
import { call, FeatherIcon, createResource } from "frappe-ui";
import { ref, nextTick, watch, computed, h } from "vue";
import { useRouter } from "vue-router";
import { createToast } from "@/utils";

const props = defineProps({
	options: {
		type: Object,
		default: {
			redirect: true,
			detailMode: false,
			afterInsert: () => {},
		},
	},
	list_field_value: {
		type: Object,
		default: {},
	},
	listPermission: {
		type: Object,
		default: {},
	},
	editMode: {
		type: Boolean,
		default: false,
	},
});

const { isManager } = usersStore();

const router = useRouter();
const show = defineModel();
const yyy = defineModel("yyy");

const emit = defineEmits(["updateList"]);

const loading = ref(false);
const title = ref(null);
const detailMode = ref(false);
const editMode = ref(false);
let _address = ref({});
let _yyy = ref({
	name: "",
	institution_name: "",
	location: "",
	training_type: "",
});

const showAddressModal = ref(false);

let doc = ref({});

async function updateyyy() {
	const old = { ...doc.value };
	const newOrg = { ..._yyy.value };

	const nameChanged = old.yyy_name !== newOrg.yyy_name;
	delete old.yyy_name;
	delete newOrg.yyy_name;

	const otherFieldChanged = JSON.stringify(old) !== JSON.stringify(newOrg);
	const values = newOrg;

	if (!nameChanged && !otherFieldChanged) {
		show.value = false;
		return;
	}

	let name;
	loading.value = true;
	// if (nameChanged) {
	//   name = await callRenameDoc()
	// }
	if (otherFieldChanged) {
		name = await callSetValue(values);
	}
	handleyyyUpdate({ name }, nameChanged);
}

async function callRenameDoc() {
	const d = await call("frappe.client.rename_doc", {
		doctype: "xxx_yyy",
		old_name: doc.value?.ho_va_ten,
		new_name: _yyy.value.ho_va_ten,
	});
	return d;
}

async function callSetValue(values) {
	try {
    if(!_yyy.value.institution_name){
      createToast({
        title: __("Error"),
        text: __("Tên cơ sở đào tạo là bắt buộc."),
        icon: "x",
        iconClasses: "text-red-600",
      });
      return;
    }
		// Hiển thị trạng thái loading
		loading.value = true;

		// Gọi API và chờ phản hồi
		const d = await call("frappe.client.set_value", {
			doctype: "ATS-Institution",
			name: _yyy.value.name,
			fieldname: values,
		});

		// Phát tín hiệu cập nhật danh sách
		emit("updateList");
    createToast({
      title: __("Success"),
      text: __("Sửa thành công"),
      icon: "check",
      iconClasses: "text-green-600",
    });

		// Trả về giá trị name từ phản hồi
		return d.name;
	} catch (error) {
		// Xử lý lỗi nếu có
		createToast({
			title: __("Error Updating Employee"),
			text: __(error.messages?.[0]),
			icon: "x",
			iconClasses: "text-red-600",
		});
		console.error("Error in callSetValue:", error);
		throw new Error("Failed to set value. Please try again later.");
	} finally {
		// Đảm bảo trạng thái loading được tắt dù có lỗi hay không
		loading.value = false;
	}
}

async function callInsertDoc() {
	try {
    if(!_yyy.value.institution_name){
      createToast({
        title: __("Error"),
        text: __("Tên cơ sở đào tạo là bắt buộc."),
        icon: "x",
        iconClasses: "text-red-600",
      });
      return;
    }
		// Bắt đầu trạng thái loading
		loading.value = true;

		// Gọi API để chèn tài liệu mới
		const doc = await call("frappe.client.insert", {
			doc: {
				doctype: "ATS-Institution",
				..._yyy.value,
			},
		});

		// Kiểm tra nếu tài liệu được tạo thành công
		if (doc.name) {
			// capture('organization_created') // Uncomment nếu cần theo dõi sự kiện
			handleyyyUpdate(doc);
      createToast({
      title: __("Success"),
      text: __("Thêm thành công"),
      icon: "check",
      iconClasses: "text-green-600",
    });
			emit("updateList");
		}
	} catch (error) {
		// Xử lý lỗi
		createToast({
			title: __("Error Creating Employee"),
			text: __(error.messages?.[0]),
			icon: "x",
			iconClasses: "text-red-600",
		});
		console.error("Error in callInsertDoc:", error);
		throw new Error("Failed to insert document. Please try again later.");
	} finally {
		// Đảm bảo trạng thái loading được tắt
		loading.value = false;
	}
}

function handleyyyUpdate(doc, renamed = false) {
	if (doc.name && (props.options.redirect || renamed)) {
		// Nếu muốn khi nhấn nút save xem được thông tin trong trang chi tiết thì thêm đoạn này này
		// router.push({
		//   name: 'yyy',
		//   params: { yyyId: doc.name },
		// })
		//
		// router.push({
		//   name: 'yyys',
		// })
	} else {
		yyy.value.reload?.();
	}
	show.value = false;
	props.options.afterInsert && props.options.afterInsert(doc);
}

const dialogOptions = computed(() => {
	let title = !editMode.value ? "Thêm tổ chức" : "Sửa thông tin";
	let size = detailMode.value ? "" : "xl";
	let actions = detailMode.value
		? []
		: [
				{
					label: editMode.value ? __("Lưu") : __("Thêm"),
					variant: "solid",
					onClick: () => (editMode.value ? updateyyy() : callInsertDoc()),
				},
			];

	return { title, size, actions };
});

const fields = computed(() => {
	let details = [
		{
			icon: OrganizationsIcon,
			name: "institution_name",
			value: _yyy.value.institution_name,
		},
	];

	return details.filter((field) => field.value);
});

const sections = createResource({
	url: "xxx.xxx.doctype.xxx_fields_layout.xxx_fields_layout.get_fields_layout",
	cache: ["quickEntryFields", "ATS-Institution"],
	params: { doctype: "ATS-Institution", type: "Quick Entry" },
	auto: true,
});

const filteredSections = computed(() => {
	let allSections = sections.data || [];
	if (!allSections.length) return [];

	return allSections;
});

watch([() => show.value, () => props.editMode], ([showVal, editModeVal]) => {
	if (!showVal) return;

	nextTick(() => {
		doc.value = yyy.value?.doc || yyy.value || {};

		if (editModeVal) {
			_yyy.value = props.list_field_value;
		} else {
			_yyy.value = { ...doc.value };
		}
	});

	editMode.value = editModeVal;
});

const showQuickEntryModal = defineModel("quickEntry");

function openQuickEntryModal() {
	showQuickEntryModal.value = true;
	nextTick(() => {
		show.value = false;
	});
}
</script>
