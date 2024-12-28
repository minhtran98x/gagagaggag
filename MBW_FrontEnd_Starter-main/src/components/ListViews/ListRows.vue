<template>
  <ListRows class="mx-3 sm:mx-5" id="list-rows">
    <ListRowCustom
      v-for="row in reactivieRows"
      :key="row.name"
      v-slot="{ idx, column, item }"
      :row="row"
    >
      <slot v-bind="{ idx, column, item, row }" />
    </ListRowCustom>
  </ListRows>
</template>

<script setup>
import { ListRows, ListRow, ListGroupHeader, ListGroupRows } from "frappe-ui";
import ListRowCustom from "../frappe-ui-custom/ListViewCustom/ListRowCustom.vue";

import { ref, computed, watch } from "vue";

const props = defineProps({
  rows: {
    type: Array,
    required: true,
  },
});

const reactivieRows = ref(props.rows);


watch(reactivieRows.value, () => {

});

watch(
  () => props.rows,
  (val) => (reactivieRows.value = val)
);
</script>
