<template>
  <q-dialog v-model="addShow" >
    <q-card bordered style="padding: 30px;width: 700px; max-width: 80vw;">
      <div style="text-align: center" class="text-h6">请输入添加学生的学号:</div>
      <q-input rounded outlined v-model="newId" label="ID" style="width: 50%;margin-left: auto;margin-right: auto"/>
      <q-btn color="blue" size="lg" align="center" style="margin-top: 30px;margin-left: 35%;margin-right: 30px" @click="addConfirm">确定</q-btn>
      <q-btn color="blue" size="lg" align="center" style="margin-top: 30px;" @click="cancel">取消</q-btn>
    </q-card>
  </q-dialog>

  <div
    class="q-pa-md"
    style="width: 72%; margin-left: auto; margin-right: auto"
  >
    <div class="text-grey text-h6" style="white-space: pre-wrap">
      {{classTime}} &nbsp;&nbsp;&nbsp;&nbsp; 授课教师：{{teacher}} &nbsp;&nbsp;&nbsp;&nbsp; 课程编号：{{classIndex}}
      <q-btn icon="add" style="margin-left: 35%" rounded color="blue" @click="add">添加学生</q-btn>
    </div>
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
      classTime: "周三第四节",
      teacher: "李红",
      classIndex: "PE089756",
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
        {"name": "video", "align": "center", "label": "上传视频数", "field": "num", sortable: true},
        {"name": "average", "align": "center", "label": "平均分", "field": "average", sortable: true},
        { "name": "check", "align": "center", "label": "操作", "field": "check" }
      ],
      "rows": [
        {"id":19231111,"name":"张三","num":8,"average":85},
        {"id":19231112,"name":"丽丝","num":4,"average":83},
        {"id":19231113,"name":"李杰","num":2,"average":90},
        {"id":19231114,"name":"司马光","num":1,"average":75},
        {"id":19231115,"name":"王瑞","num":3,"average":88},
        {"id":19231116,"name":"段思杰","num":2,"average":95},
        {"id":19231117,"name":"李金黄","num":5,"average":67},
        {"id":19231118,"name":"刘可欣","num":5,"average":87},
        {"id":19231119,"name":"段锐恒","num":6,"average":45},
        {"id":19231120,"name":"马源信","num":8,"average":92},
        {"id":19231121,"name":"韩少黄","num":8,"average":90},
      ],
      "pagesNumber": computed(() => Math.ceil(this.rows.length / pagination.value.rowsPerPage)),
      addShow: false,
      newId: ''
    };
  },
  methods: {
    add(){
      this.addShow = true
    },
    addConfirm(){
      if(this.newId !== "") {
        alert("添加成功")
        this.addShow = false
      }
      else {
        alert("请输入要添加的学号")
      }
    },
    cancel(){
      this.addShow=false
    }
  }
}
</script>

<style scoped>

</style>
