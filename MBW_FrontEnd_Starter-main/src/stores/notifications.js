import { defineStore } from 'pinia'
import { createResource } from 'frappe-ui'
import { computed, ref } from 'vue'

export const notificationsStore = defineStore('social-insurance-notifications', () => {
  let visible = ref(false)

  function toggle() {
    visible.value = !visible.value
  }

  return {
    visible,
    toggle,
  }
})
