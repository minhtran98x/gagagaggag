import { defineStore } from "pinia";

export const useFieldStore = defineStore("childTableField", {
	state: () => ({
		childTableField: "", // Giá trị chiều rộng khối cha
		timestamp: null,
        actionType: null, // "edit" hoặc "delete"
	}),
	actions: {
		setChildTableField(id, action) {
			this.childTableField = id;
            this.actionType = action;
			this.timestamp = Date.now();
		},
		getChildTableField() {
			return this.childTableField;
		},
	},
});
