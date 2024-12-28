<template>
  <div class="flex flex-col gap-1.5 border-b sm:px-6 py-3 px-4">
    <div
      v-for="field in employeeSection"
      :key="field.label"
      class="flex items-center gap-2 text-base leading-5"
    >
      <div class="sm:w-[106px] w-36 text-sm text-gray-600">
        {{ __(field.label) }}
      </div>
      <div class="grid min-h-[28px] items-center">
        <Tooltip v-if="field.tooltipText" :text="__(field.tooltipText)">
          <div class="ml-2 cursor-pointer">
            <Badge
              v-if="field.type === 'Badge'"
              class="-ml-1"
              :label="field.value"
              variant="subtle"
              :theme="field.color"
            />
            <div v-else>{{ field.value }}</div>
          </div>
        </Tooltip>
        <Dropdown
          class="form-control"
          v-if="field.type === 'Select'"
          :options="field.options"
        >
          <template #default="{ open }">
            <Button :label="field.value">
              <template #suffix>
                <FeatherIcon
                  :name="open ? 'chevron-up' : 'chevron-down'"
                  class="h-4"
                />
              </template>
            </Button>
          </template>
        </Dropdown>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Tooltip, Badge, Dropdown } from "frappe-ui";
import { computed, defineModel } from "vue";

const data = defineModel();

// Nhóm dữ liệu hiển thị các trường yêu cầu từ employeeData
let employeeSection = computed(() => {
  let sections = [
    {
      label: "Họ và tên",
      value: data.value.employee_name || "N/A",
      type: "Text",
      tooltipText: data.value.employee_name || "N/A",
    },
    {
      label: "Số CCCD/ĐDCN/Hộ chiếu",
      value: data.value.so_cccd_ddcn_ho_chieu || "N/A",
      type: "Text",
      tooltipText: data.value.employee_name || "N/A",
    },
    {
      label: "Ngày sinh",
      value: formattedDateTooltip(data.value.date_of_birth) || "N/A",
      type: "Text",
      tooltipText: formattedDateTooltip(data.value.date_of_birth) || "N/A",
    },
    {
      label: "Giới tính",
      value: data.value.gender || "N/A",
      type: "Text",
      tooltipText: data.value.gender || "N/A",
    },
    {
      label: "Quốc tịch",
      value: data.value.quoc_tich || "N/A",
      type: "Text",
      tooltipText: data.value.employee_name || "N/A",
    },
    {
      label: "Dân tộc",
      value: data.value.dan_toc || "N/A",
      type: "Text",
      tooltipText: data.value.employee_name || "N/A",
    },
    {
      label: "Bộ phận/Phòng ban",
      value: formatDepartment(data.value.department) || "N/A",
      type: "Text",
      tooltipText: formatDepartment(data.value.department) || "N/A",
    },
    {
      label: "Mức Lương",
      value: formatCurrency(data.value.muc_luong) || "N/A",
      type: "Text",
      tooltipText:  formatCurrency(data.value.muc_luong)|| "N/A",
    },
    {
      label: "Tỷ lệ đóng",
      value: formatTiLeDong(data.value.ty_le_dong) || "N/A",
      type: "Text",
      tooltipText: formatTiLeDong(data.value.ty_le_dong) || "N/A",
    },
  ];
  return sections;
});
function formattedDateTooltip(dateStr) {
  const [year, month, day] = dateStr.split("-");
  return `${day}/${month}/${year}`;
}
function formatCurrency(value) {
    return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".") + " VNĐ";
}
function formatTiLeDong(value) {
    return value + "%";
}
function formatDepartment(value) {
    if (value ==="i4g3etoq8d") {
        return "Phòng nhân sự"
    }
    if (value ==="i437j045je") {
        return "Phòng IT"
    }
    else {
        return "Phòng kế toán"
    }
}
function formatChucVu(value) {
    if (value ==="rvgfnjpmq2") {
        return "Nhân viên Kế toán"
    }
    else if (value ==="rvdeu5vokh") {
        return "Nhân viên kinh doanh"
    }
    else if (value ==="rvasnlk1a5") {
        return "Nhân viên hợp đồng"
    }
    else if (value ==="rv8nq8skph") {
        return "Giám đốc Kinh doanh"
    }
    else if (value ==="rv6fe4lk2b") {
        return "Trưởng phòng lập trình"
    }
    else if (value ==="rv46l9gevg") {
        return "Trưởng nhóm kinh doanh"
    }
    else if (value ==="ruvet3r9ku") {
        return "Nhân viên kinh doanh"
    }
    else if (value ==="rus8obaj5p") {
        return "Nhân viên nhân sự"
    }
    else if (value ==="ruqevcvn62") {
        return "Trưởng nhóm Marketing"
    }
    else if (value ==="ruo3te09ek") {
        return "Nhân viên triển khai và hỗ trợ"
    }
    else if (value ==="rum3sn69fj") {
        return "Trưởng nhóm lập trình"
    }
    else if (value ==="rujmqsan0i") {
        return "Nhân viên Tuyển dụng & đào tạo"
    }
    else if (value ==="ruhdon8puv") {
        return "Nhân viên lập trình"
    }
    else if (value ==="ruf6jk41cj") {
        return "Nhân viên UX/UI"
    }
    else {
        return "Phòng kế toán"
    }
}

function formatBenhVien(value) {
    if (value ==="rqeo2uq443") {
        return "Bệnh viện Gia Định"
    }
    else if (value ==="rot7vuf9kk") {
        return "Bệnh viện 108"
    }
    else if (value ==="roh4l413b1") {
        return "Bệnh viện Bạch Mai"
    }
    else if (value ==="rntpnc0g71") {
        return "Bệnh viện Hoàn Mỹ"
    }
    else if (value ==="r7320s5vhk") {
        return "Bệnh viện Nhi đồng 2"
    }
    else if (value ==="r6vemn9lvg") {
        return "Bệnh viện Chỡ Rẫy"
    }
    else if (value ==="r6rf1t9o8t") {
        return "Bệnh viện Việt Đức"
    }
    else if (value ==="r6mng2ghbc") {
        return "Bệnh viện Vinmec"
    }
    else {
        return "Bệnh viện Bạch Mai"
    }
}
</script>

<style scoped>
:deep(.form-control button) {
  border-color: transparent;
  background: white;
}
</style>
