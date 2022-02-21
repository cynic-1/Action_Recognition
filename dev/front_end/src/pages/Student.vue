<template>
  <div
    class="q-pa-md"
    style="width: 72%; margin-left: auto; margin-right: auto"
  >

    <q-table
      v-model:pagination="pagination"
      :rows="rows"
      :columns="columns"
      row-key="name"
      hide-pagination
    >
      <template v-slot:body-cell-title="props">
        <q-td :props="props">
          <div class="my-table-details" style="cursor: pointer" @click="check(props.row.id)">
            {{props.value}}
          </div>
        </q-td>
      </template>

      <template v-slot:body-cell-author="props">
        <q-td :props="props">
          <div class="my-table-details2">
            <span v-for="item in props.value" :key="item">{{item}}&nbsp;&nbsp;</span>
          </div>
        </q-td>
      </template>

      <template v-slot:body-cell-org="props">
        <q-td :props="props">
          <div class="my-table-details2">
            {{props.value}}
          </div>
        </q-td>
      </template>

      <template v-slot:body-cell-time="props">
        <q-td :props="props">
          <div class="my-table-details2">
            {{props.value}}
          </div>
        </q-td>
      </template>

      <template v-slot:body-cell-keyword="props">
        <q-td :props="props">
          <div class="my-table-details">
            <span v-for="item in props.value" :key="item">{{item}}&nbsp;&nbsp;</span>
          </div>
        </q-td>
      </template>

      <template v-slot:body-cell-check="props">
        <q-td :props="props">
          <q-btn flat rounded to="/videos">查看详情</q-btn>
        </q-td>
      </template>
    </q-table>

    <div class="row justify-center q-mt-md">
      <q-pagination
        v-model="pagination.page"
        color="grey-8"
        :max="pagesNumber"
        :max-pages="6"
        size="sm"
      />
    </div>
  </div>
</template>

<script>
import { computed, ref } from "vue";
export default {
  name: "Student",
  data() {
    const pagination = ref({
      "sortBy": "desc",
      "descending": false,
      "page": 1,
      "rowsPerPage": 20
      // rowsNumber: xx if getting data from a server
    });
    return {
      pagination,
      "columns": [
        {
          "name": "id",
          "required": true,
          "label": "学号",
          "align": "center",
          "field": row => row.id,
          "format": val => `${val}`
        },
        {"name": "name", "align": "center", "label": "姓名", "field": "name"},
        {"name": "teacher", "align": "center", "label": "授课教师", "field": "teacher"},
        {"name": "video", "align": "center", "label": "上传视频数", "field": "num", sortable: true},
        {"name": "average", "align": "center", "label": "平均分", "field": "average", sortable: true},
        { "name": "check", "align": "center", "label": "操作", "field": "check" }
      ],
      "rows": [
        {"id":19231111,"name":"张三","teacher":"李红","num":8,"average":85},
        {"id":19231112,"name":"丽丝","teacher":"李红","num":4,"average":83},
        {"id":19231113,"name":"李杰","teacher":"李红","num":2,"average":90},
        {"id":19231114,"name":"司马光","teacher":"李红","num":1,"average":75},
        {"id":19231115,"name":"王瑞","teacher":"李红","num":3,"average":88},
        {"id":19231116,"name":"段思杰","teacher":"李红","num":2,"average":95},
        {"id":19231117,"name":"李金黄","teacher":"李红","num":5,"average":67},
        {"id":19231118,"name":"刘可欣","teacher":"李红","num":5,"average":87},
        {"id":19231119,"name":"段锐恒","teacher":"李红","num":6,"average":45},
        {"id":19231120,"name":"马源信","teacher":"李红","num":8,"average":92},
        {"id":19231121,"name":"韩少黄","teacher":"李红","num":8,"average":90},
      ],
      "pagesNumber": computed(() => Math.ceil(this.rows.length / pagination.value.rowsPerPage)),
      "method": 1,
      "line": "",
      "topAuthor": [],
      "topKeyWord": [],
      "topDate": [],
      "topSchool": [],
      "relatedPaper": []
    };
  }
}
</script>

<style scoped>

</style>
