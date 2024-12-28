<template>
  <Dropdown v-if="optionsMore.length" :options="optionsMore">
    <Button icon="more-horizontal"></Button>
  </Dropdown>
  <Button
    v-if="actions?.write"
    variant="solid"
    :ref_for="true"
    theme="gray"
    size="sm"
    label="Save"
    @click="handleSave"
  >
  </Button>
  <template v-if="!optionsTransitions.length">
    <Button
      v-if="actions?.submit"
      variant="solid"
      :ref_for="true"
      theme="gray"
      size="sm"
      label="Submit"
      @click="() => handleShowModalConfirm('Submit')"
    >
    </Button>
    <Button
      v-if="actions?.cancel"
      variant="solid"
      :ref_for="true"
      theme="red"
      size="sm"
      label="Cancel"
      @click="() => handleShowModalConfirm('Cancel')"
    >
    </Button>
    <Button
      v-if="actions?.amend"
      variant="solid"
      :ref_for="true"
      theme="gray"
      size="sm"
      label="Amend"
      @click="handleAmend"
    >
    </Button>
  </template>
  <Dropdown
    v-if="optionsTransitions.length && !actions?.write"
    :options="optionsTransitions"
  >
    <Button variant="solid" label="Actions" iconRight="chevron-down"></Button>
  </Dropdown>

  <!-- Modal -->
  <ConfirmModal v-model="showModalConfirm" @confirm="handleConfirmModal">
    <template #title>
      <h3>{{ __("Confirm") }}</h3>
    </template>
    <template #content>
      <p v-if="modalAction == 'Submit'">
        {{ __("Permanently Submit {0}", [docname]) }}?
      </p>
      <p v-else-if="modalAction == 'Cancel'">
        {{ __("Permanently delete {0}", [docname]) }}?
      </p>
      <p v-else-if="modalAction == 'Delete'">
        {{ __("Permanently Cancel {0}", [docname]) }}?
      </p>
    </template>
  </ConfirmModal>
</template>

<script setup>
import { onMounted, ref, watch } from "vue";
import { Dropdown, createResource, call } from "frappe-ui";
import { createToast } from "@/utils";
import { useRouter } from "vue-router";
import ConfirmModal from "@/components/Modals/ConfirmModal.vue";

const router = useRouter();

const props = defineProps({
  doctype: {
    type: String,
    required: true,
  },
  isNew: {
    type: Boolean,
    default: false,
  },
  doc: {
    type: Object,
    default: {},
  },
  deleteRedirect: {
    type: String,
    default: "",
  },
  createRedirect: {
    type: String,
    default: "",
  },
  onSave: {
    type: Function,
  },
  reloadDoc: {
    type: Function,
  },
});

const actions = ref({
  write: 0,
  submit: 0,
  cancel: 0,
  amend: 0,
});
const optionsTransitions = ref([]);
const optionsMore = ref([]);
const docname = ref("");
const showModalConfirm = ref(false);
const modalAction = ref("Submit");
const configDoc = defineModel("configDoc");
const isDirty = defineModel("isDirty");

const docInfo = createResource({
  url: "xxx.api.workflow.get_doc_info",
  params: {},
  onSuccess: (data) => {
    configDoc.value = data;
    updateActions(data);
  },
});

function updateActions(data) {
  // cập nhật lại các quyền button cho user
  let newActions = {
    write: 0,
    submit: 0,
    cancel: 0,
    amend: 0,
  };
  let newOptionsMore = [];

  let docstatus = props.doc?.docstatus || 0;
  if (data?.transitions) {
    optionsTransitions.value = data?.transitions.map((el) => ({
      label: el.action,
      onClick: () => {
        handleWorkflow(el.action);
      },
    }));
  }

  let permissions = data?.permissions;
  if (permissions?.read) {
    if (props.isNew) {
      if (permissions?.create && permissions?.write) {
        newActions.write = 1;
      }
    } else {
      if (permissions?.write) {
        if (
          !data?.has_workflow ||
          (data?.has_workflow && data?.allow_state_edit)
        ) {
          if ((docstatus != 2 && isDirty.value) || !data?.is_submittable) {
            newActions.write = 1;
          }
          if (docstatus == 2 && !data?.is_amended) {
            newActions.amend = 1;
          }
        }
        if (
          docstatus == 0 &&
          permissions?.submit &&
          !data?.has_workflow &&
          !isDirty.value
        ) {
          newActions.submit = 1;
        }
        if (docstatus == 1 && permissions?.cancel && data?.allow_sate_cancel) {
          newActions.cancel = 1;
        }
      }

      if (docstatus != 1 && permissions?.delete) {
        newOptionsMore.push({
          label: "Delete",
          onClick: () => {
            handleShowModalConfirm("Delete");
          },
        });
      }
    }

    optionsMore.value = newOptionsMore;
    actions.value = newActions;
  }
}

watch(docname, (val) => {
  if (props.isNew || (!props.isNew && val)) {
    docInfo.update({
      params: {
        doctype: props.doctype,
        docname: docname,
      },
    });
    docInfo.fetch();
  }
});

watch(
  () => JSON.stringify(props.doc),
  (newVal, oldVal) => {
    docname.value = props.doc?.name;
    if (!props.isNew) {
      if (!["undefined", "{}"].includes(oldVal) && newVal != oldVal) {
        isDirty.value = true;
      }
    }
    // updateActions(docInfo.data);
  },
  { immediate: true }
);

watch(
  isDirty,
  (val) => {
    updateActions(docInfo.data);
  },
  { immediate: true }
);

function refreshActions() {
  props.reloadDoc();
  docInfo.fetch();
  updateActions(docInfo.data);
}

function handleSave() {
  // kiem tra doc co thay doi khong
  if (isDirty.value) {
    // Gọi hàm lưu từ cha
    props.onSave();
  } else {
    createToast({
      title: __("No changes in document"),
      icon: "alert-circle",
      iconClasses: "text-orange-600",
    });
  }
}

function handleShowModalConfirm(typeModal) {
  showModalConfirm.value = true;
  modalAction.value = typeModal;
}
function handleConfirmModal() {
  if (modalAction.value == "Submit") {
    handleSubmit();
  } else if (modalAction.value == "Cancel") {
    handleCancel();
  } else if (modalAction.value == "Delete") {
    handleDelete();
  }
}

async function handleSubmit() {
  let newDoc = { ...props.doc };
  delete newDoc.fields_meta;

  try {
    await call("frappe.desk.form.save.savedocs", {
      doc: JSON.stringify(newDoc),
      action: "Submit",
    });

    createToast({
      title: __("Submitted"),
      icon: "check",
      iconClasses: "text-green-600",
    });
    refreshActions();
  } catch (err) {
    createToast({
      title: __("An error occurred."),
      text: err.messages[0],
      icon: "x",
      iconClasses: "text-red-600",
    });
  }
}
async function handleCancel() {
  try {
    await call("frappe.desk.form.save.cancel", {
      doctype: props.doctype,
      name: docname.value,
    });

    createToast({
      title: __("Cancelled"),
      icon: "x",
      iconClasses: "text-red-600",
    });
    refreshActions();
  } catch (err) {
    createToast({
      title: __("An error occurred."),
      text: err.messages[0],
      icon: "x",
      iconClasses: "text-red-600",
    });
  }
}
async function handleDelete() {
  try {
    await call("frappe.client.delete", {
      doctype: props.doctype,
      name: docname.value,
    });
    router.push(props.deleteRedirect);
  } catch (err) {
    createToast({
      title: __("An error occurred."),
      text: err.messages[0],
      icon: "x",
      iconClasses: "text-red-600",
    });
  }
}
async function handleWorkflow(action) {
  let newDoc = { ...props.doc };
  delete newDoc.fields_meta;

  try {
    await call("frappe.model.workflow.apply_workflow", {
      doc: JSON.stringify(newDoc),
      action: action,
    });

    refreshActions();
  } catch (err) {
    createToast({
      title: __("An error occurred."),
      text: err.messages[0],
      icon: "x",
      iconClasses: "text-red-600",
    });
  }
}

function handleAmend() {
  router.push(props.createRedirect + `?amended_from=${docname.value}`);
}
</script>
