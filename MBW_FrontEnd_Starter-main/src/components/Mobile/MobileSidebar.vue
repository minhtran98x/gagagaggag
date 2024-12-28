<template>
  <TransitionRoot :show="sidebarOpened">
    <Dialog as="div" @close="sidebarOpened = false" class="fixed inset-0 z-40">
      <TransitionChild
        as="template"
        enter="transition ease-in-out duration-200 transform"
        enter-from="-translate-x-full"
        enter-to="translate-x-0"
        leave="transition ease-in-out duration-200 transform"
        leave-from="translate-x-0"
        leave-to="-translate-x-full"
      >
        <div
          class="relative z-10 flex h-full w-[260px] flex-col justify-between border-r bg-gray-50 transition-all duration-300 ease-in-out"
        >
          <div><UserDropdown class="p-2" /></div>
          <div class="flex-1 overflow-y-auto">
            <div v-for="view in allViews" :key="view.label">
              <Section
                :label="view.name"
                :hideLabel="view.hideLabel"
                :isOpened="view.opened"
              >
                <template #header="{ opened, hide, toggle }">
                  <div
                    v-if="!hide"
                    class="ml-2 mt-4 flex h-7 w-auto cursor-pointer gap-1.5 px-1 text-base font-medium text-gray-600 opacity-100 transition-all duration-300 ease-in-out"
                    @click="toggle()"
                  >
                    <FeatherIcon
                      name="chevron-right"
                      class="h-4 text-gray-900 transition-all duration-300 ease-in-out"
                      :class="{ 'rotate-90': opened }"
                    />
                    <span>{{ __(view.name) }}</span>
                  </div>
                </template>
                <nav class="flex flex-col">
                  <SidebarLink
                    v-for="link in view.views"
                    :icon="link.icon"
                    :label="__(link.label)"
                    :to="link.to"
                    class="mx-2 my-0.5"
                  />
                </nav>
              </Section>
            </div>
          </div>
        </div>
      </TransitionChild>
      <TransitionChild
        as="template"
        enter="transition-opacity ease-linear duration-200"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="transition-opacity ease-linear duration-200"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <DialogOverlay class="fixed inset-0 bg-gray-600 bg-opacity-50" />
      </TransitionChild>
    </Dialog>
  </TransitionRoot>
</template>
<script setup>
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogOverlay,
} from '@headlessui/vue'
import Section from '@/components/Section.vue'
import PinIcon from '@/components/Icons/PinIcon.vue'
import UserDropdown from '@/components/UserDropdown.vue'
import ContactsIcon from '@/components/Icons/ContactsIcon.vue'
import SidebarLink from '@/components/SidebarLink.vue'
import { computed, h } from 'vue'
import { mobileSidebarOpened as sidebarOpened } from '@/composables/settings'

const links = [
  {
    label: 'Employees',
    icon: ContactsIcon,
    to: 'Employees',
  }
]

const allViews = computed(() => {
  let _views = [
    {
      name: 'All Views',
      hideLabel: true,
      opened: true,
      views: links,
    },
  ]
  return _views
})

function getIcon(routeName, icon) {
  if (icon) return h('div', { class: 'size-auto' }, icon)

  switch (routeName) {
    case 'Contacts':
      return ContactsIcon
    default:
      return PinIcon
  }
}
</script>
