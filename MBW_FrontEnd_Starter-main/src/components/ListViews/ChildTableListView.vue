<template>
  <ListView
    :class="$attrs.class"
    :columns="columns"
    :rows="rows"
    :options="{
      selectable: options.selectable,
      showTooltip: options.showTooltip,
      resizeColumn: options.resizeColumn,
    }"
    row-key="name"
  >
    <ListSelectBanner>
      <template #actions="{ selections, unselectAll }">
        {{ console.log(selections) }}
        <Dropdown
          :options="listBulkActionsRef.bulkActions(selections, unselectAll)"
        >
          <Button icon="more-horizontal" variant="ghost" />
        </Dropdown>
      </template>
    </ListSelectBanner>
  </ListView>
  <ListBulkActions
    ref="listBulkActionsRef"
    v-model="list"
    doctype="IVAN_Employee"
    :options="{
      hideAssign: true,
    }"
  />
</template>

<script setup>
import HeartIcon from "@/components/Icons/HeartIcon.vue";
//   import IndicatorIcon from '@/components/Icons/IndicatorIcon.vue'
//   import PhoneIcon from '@/components/Icons/PhoneIcon.vue'
//   import MultipleAvatar from '@/components/MultipleAvatar.vue'
import ListBulkActions from "@/components/ListBulkActions.vue";

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
  ListRows
} from "frappe-ui";
import { sessionStore } from "@/stores/session";
import { ref, computed, watch, onMounted } from "vue";
import { useRoute } from "vue-router";

const props = defineProps({
  rows: {
    type: Array,
    required: true,
  },
  columns: {
    type: Array,
    required: true,
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
console.log(props.rows);

const emit = defineEmits([
  "loadMore",
  "updatePageCount",
  "columnWidthUpdated",
  "applyFilter",
  "applyLikeFilter",
  "likeDoc",
]);

const route = useRoute();

const pageLengthCount = defineModel();
const list = defineModel("list");

const { user } = sessionStore();

const listBulkActionsRef = ref(null);
console.log(listBulkActionsRef);

defineExpose({
  customListActions: computed(
    () => listBulkActionsRef.value?.customListActions
  ),
});
</script>
