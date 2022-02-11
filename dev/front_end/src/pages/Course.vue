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
                    <q-btn flat rounded>查看详情</q-btn>
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
  name: "Course",
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
          "name": "date",
          "required": true,
          "label": "上课时间",
          "align": "center",
          "field": row => row.date,
          "format": val => `${val}`
        },
        {"name": "teacher", "align": "center", "label": "授课教师", "field": "teacher"},
        {"name": "total", "align": "center", "label": "应到人数", "field": "total", sortable: true},
        {"name": "actual", "align": "center", "label": "实到人数", "field": "actual", sortable: true},
        { "name": "check", "align": "center", "label": "操作", "field": "check" }
      ],
      "rows": [
        {"date":"2021.07.03","teacher":"李红","total":56,"actual":56},
        {"date":"2021.07.03","teacher":"李红","total":56,"actual":56},
        {"date":"2021.07.03","teacher":"李红","total":56,"actual":56},
        {"date":"2021.07.03","teacher":"李红","total":56,"actual":56},
        {"date":"2021.07.03","teacher":"李红","total":56,"actual":56},
        {"date":"2021.07.03","teacher":"李红","total":56,"actual":56},
        {"date":"2021.07.03","teacher":"李红","total":56,"actual":56},
        {"date":"2021.07.03","teacher":"李红","total":56,"actual":56},
        {"date":"2021.07.03","teacher":"李红","total":56,"actual":56},
        {"date":"2021.07.03","teacher":"李红","total":56,"actual":56},

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
