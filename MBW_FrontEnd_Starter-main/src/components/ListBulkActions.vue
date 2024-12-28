<template>
  <EditValueModal
    v-if="showEditModal"
    v-model="showEditModal"
    :doctype="doctype"
    :selectedValues="selectedValues"
    @reload="reload"
  />
  <AssignmentModal
    v-if="showAssignmentModal"
    v-model="showAssignmentModal"
    v-model:assignees="bulkAssignees"
    :docs="selectedValues"
    :doctype="doctype"
    @reload="reload"
  />
</template>

<script setup>
import EditValueModal from '@/components/Modals/EditValueModal.vue'
import AssignmentModal from '@/components/Modals/AssignmentModal.vue'
import { setupListCustomizations, createToast } from '@/utils'
import { globalStore } from '@/stores/global'
import { capture } from '@/telemetry'
import { call,createResource } from 'frappe-ui'
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const props = defineProps({
  doctype: {
    type: String,
    default: '',
  },
  options: {
    type: Object,
    default: () => ({
      hideEdit: false,
      hideDelete: false,
      hideAssign: false,
    }),
  },
  eProfileId: {
    type: String,
    default: ''
  },
})

const emit = defineEmits(['eventhiddenModal'])
const list = defineModel()
const route = useRoute()
const router = useRouter()

const { $dialog, $socket } = globalStore()

const showEditModal = ref(false)
const selectedValues = ref([])
const unselectAllAction = ref(() => {})

function editValues(selections, unselectAll) {
  selectedValues.value = selections
  showEditModal.value = true
  unselectAllAction.value = unselectAll
}

// function convertToDeal(selections, unselectAll) {
//   $dialog({
//     title: __('Convert to Deal'),
//     message: __('Are you sure you want to convert {0} Lead(s) to Deal(s)?', [
//       selections.size,
//     ]),
//     variant: 'solid',
//     theme: 'blue',
//     actions: [
//       {
//         label: __('Convert'),
//         variant: 'solid',
//         onClick: (close) => {
//           capture('bulk_convert_to_deal')
//           Array.from(selections).forEach((name) => {
//             call('crm.fcrm.doctype.crm_lead.crm_lead.convert_to_deal', {
//               lead: name,
//             }).then(() => {
//               createToast({
//                 title: __('Converted successfully'),
//                 icon: 'check',
//                 iconClasses: 'text-green-600',
//               })
//               list.value.reload()
//               unselectAll()
//               close()
//             })
//           })
//         },
//       },
//     ],
//   })
// }

// function convertToProfile(selections, unselectAll){
//   // Chuyển `selections` từ `Set` thành mảng
//   const selectedIds = Array.from(selections);
//   // Gọi API với danh sách ID đã chọn
//   const actionIns = createResource({
//     url: "i_van.mbw_i_van.doctype.ivan_document.api.create_profile_records",
//     method: 'POST',
//     params: {
//       profile_id: props.eProfileId,
//       list_employee: selectedIds, // Truyền danh sách ID bản ghi đã chọn vào params
//     },
//     onSuccess(data) {
//       // Sử dung emit để truyền trạng thái lên component cha để đóng modal list nhân viên và load lại data trên các tab tờ khai
//       emit('eventStatusUpdateEmployee', "Success");
//       createToast({
//         title: __("Cập nhật người lao động thành công."),
//         icon: "check",
//         iconClasses: "text-green-800",
//       });

//       // Tải lại danh sách sau khi cập nhật
//       list.value.reload();
//       // Bỏ chọn các bản ghi
//       unselectAll();
//     },
//   });
//   actionIns.fetch();
// }

function deleteValues(selections, unselectAll) {
  $dialog({
    title: __('Delete'),
    message: __('Are you sure you want to delete {0} item(s)?', [
      selections.size,
    ]),
    variant: 'solid',
    theme: 'red',
    actions: [
      {
        label: __('Delete'),
        variant: 'solid',
        theme: 'red',
        onClick: (close) => {
          capture('bulk_delete')
          call('frappe.desk.reportview.delete_items', {
            items: JSON.stringify(Array.from(selections)),
            doctype: props.doctype,
          }).then(() => {
            createToast({
              title: __('Deleted successfully'),
              icon: 'check',
              iconClasses: 'text-green-600',
            })
            unselectAll()
            list.value.reload()
            close()
          })
        },
      },
    ],
  })
}

const showAssignmentModal = ref(false)
const bulkAssignees = ref([])

function assignValues(selections, unselectAll) {
  showAssignmentModal.value = true
  selectedValues.value = selections
  unselectAllAction.value = unselectAll
}

function clearAssignemnts(selections, unselectAll) {
  $dialog({
    title: __('Clear Assignment'),
    message: __('Are you sure you want to clear assignment for {0} item(s)?', [
      selections.size,
    ]),
    variant: 'solid',
    theme: 'red',
    actions: [
      {
        label: __('Clear Assignment'),
        variant: 'solid',
        theme: 'red',
        onClick: (close) => {
          capture('bulk_clear_assignment')
          call('frappe.desk.form.assign_to.remove_multiple', {
            doctype: props.doctype,
            names: JSON.stringify(Array.from(selections)),
            ignore_permissions: true,
          }).then(() => {
            createToast({
              title: __('Assignment cleared successfully'),
              icon: 'check',
              iconClasses: 'text-green-600',
            })
            reload(unselectAll)
            close()
          })
        },
      },
    ],
  })
}

const customBulkActions = ref([])
const customListActions = ref([])

function bulkActions(selections, unselectAll) {
  let actions = []


  // if (props.doctype === 'IVAN_Employee') {
  //   actions.push({
  //     label: __('Save'),
  //     onClick: () => convertToProfile(selections, unselectAll),
  //   })
  // }

  if (!props.options.hideEdit) {
    actions.push({
      label: __('Edit'),
      onClick: () => editValues(selections, unselectAll),
    })
  }

  if (!props.options.hideDelete) {
    actions.push({
      label: __('Delete'),
      onClick: () => deleteValues(selections, unselectAll),
    })
  }

  if (!props.options.hideAssign) {
    actions.push({
      label: __('Assign To'),
      onClick: () => assignValues(selections, unselectAll),
    })
    actions.push({
      label: __('Clear Assignment'),
      onClick: () => clearAssignemnts(selections, unselectAll),
    })
  }

  // if (props.doctype === 'CRM Lead') {
  //   actions.push({
  //     label: __('Convert to Deal'),
  //     onClick: () => convertToDeal(selections, unselectAll),
  //   })
  // }

  customBulkActions.value.forEach((action) => {
    actions.push({
      label: __(action.label),
      onClick: () =>
        action.onClick({
          list: list.value,
          selections,
          unselectAll,
          call,
          createToast,
          $dialog,
          router,
        }),
    })
  })
  return actions
}

function reload(unselectAll) {
  unselectAllAction.value?.()
  unselectAll?.()
  list.value?.reload()
}

onMounted(async () => {
  if (!list.value?.data) return
  let customization = await setupListCustomizations(list.value.data, {
    list: list.value,
    call,
    createToast,
    $dialog,
    $socket,
    router,
  })
  customBulkActions.value =
    customization?.bulkActions || list.value?.data?.bulkActions || []
  customListActions.value =
    customization?.actions || list.value?.data?.listActions || []
})

defineExpose({
  bulkActions,
  customListActions,
})
</script>
