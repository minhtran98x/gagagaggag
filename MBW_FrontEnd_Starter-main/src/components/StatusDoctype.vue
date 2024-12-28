<template>
  <span class="text-sm rounded-md py-1 px-2" :style="style">
    {{ status }}
  </span>
</template>

<script setup>
import { ref, watch } from "vue";
const props = defineProps({
  configDoc: {
    type: Object,
    default: {},
  },
  doc: {
    type: Object,
    default: {},
  },
  isDirty: {
    type: Boolean,
  },
});

const status = ref("");
const style = ref({});

watch(
  [() => props.doc, () => props.configDoc, () => props.isDirty],
  ([newDoc, newConfig, newIsDirty]) => {
    // xử lý các trạng thái cho bản ghi
    if (JSON.stringify(newConfig) != "{}") {
      let docstatus = newDoc?.docstatus;
      if (!newConfig?.is_submittable) {
        docstatus = -1;
      }
      if (newConfig?.has_workflow && newConfig?.override_status == 0) {
        docstatus = newConfig?.workflow_state;
      }
      if (
        (newConfig?.has_workflow && newConfig?.allow_state_edit) ||
        !newConfig?.has_workflow
      ) {
        if (newConfig?.permissions?.write && newIsDirty) {
          docstatus = 3;
        }
      }
      status.value = newConfig?.lst_status[docstatus]?.label;
      style.value = {
        color: newConfig?.lst_status[docstatus]?.color,
        background: newConfig?.lst_status[docstatus]?.background,
      };
    }
  },
  { immediate: true, deep: true }
);
</script>
