<template>
  <div class="login">
    <div class="card">
      <div class="front">
        <div class="items-center q-mx-md">
          <q-form
            ref="form"
            v-model="valid"
            lazy-validation
          >
            <q-icon
              size="100px"
              name="person_add"
            /><br>
            <div>
              <q-input
                v-model="id"
                :rules="idRules"
                label="学号/工号"
                required
              >
                <template #label>
                  <div class="text-h5">
                    学号/工号
                  </div>
                </template>
              </q-input>

              <q-input
                v-model="name"
                label=""
                required
                maxlength="5"
              >
                <template #label>
                  <div class="text-h5">
                    姓名
                  </div>
                </template>
              </q-input>

              <q-input
                v-model="college"
                label=""
                required
              >
                <template #label>
                  <div class="text-h5">
                    学院
                  </div>
                </template>
              </q-input>

              <q-input
                v-model="password"
                :rules="[passwordRules]"
                :type="show2 ? 'text' : 'password'"
                label="密码"
                required
              >
                <template #append>
                  <q-avatar v-if="show2">
                    <q-btn
                      icon="visibility_off"
                      round
                      size="14px"
                      @click="show2 = !show2"
                    />
                  </q-avatar>
                  <q-avatar v-else>
                    <q-btn
                      icon="visibility"
                      round
                      size="14px"
                      @click="show2 = !show2"
                    />
                  </q-avatar>
                </template>
                <template #label>
                  <div class="text-h5">
                    密码
                  </div>
                </template>
              </q-input>

              <q-input
                v-model="rePassword"
                :type="show3 ? 'text' : 'password'"
                :rules="[passwordRules, affirmPass]"
                lazy-rules
                label="确认密码"
                type="password"
                required
              >
                <template #append>
                  <q-avatar v-if="show3">
                    <q-btn
                      icon="visibility_off"
                      round
                      size="14px"
                      @click="show3 = !show3"
                    />
                  </q-avatar>
                  <q-avatar v-else>
                    <q-btn
                      icon="visibility"
                      round
                      size="14px"
                      @click="show3 = !show3"
                    />
                  </q-avatar>
                </template>
                <template #label>
                  <div class="text-h5">
                    确认密码
                  </div>
                </template>
              </q-input>


              <q-input
                v-model="Email"
                :rules="emailRules"
                label="邮箱"
                type="email"
                lazy-rules
                required
              >
                <template #label>
                  <div class="text-h5">
                    邮箱
                  </div>
                </template>
              </q-input>

              <q-select
                v-model="role"
                :options="options"
                label="身份"
              >
                <template #label>
                  <div class="text-h5">
                    身份
                  </div>
                </template>
              </q-select>

              <q-btn
                :disabled="!valid"
                class="button"
                large
                @click="Register"
              >
                <p class="login_">
                  注册
                </p>
              </q-btn>
            </div>
          </q-form>
        </div>
        <div>
          <div class="row">
            <div class="col-12 items-center">
              <q-btn
                flat
                color="primary"
                class="return"
                to="/login"
              >
                登录
              </q-btn>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
    "data": () => ({
        "show2": false,
        "show3": false,
        "valid": true,
        "id": "",
        "idRules": [(v) => !!v || "ID is required"],
        "name": "",
        "college": "",
        "password": "",
        "passwordRules": (v) => !!v || "请填写密码",
        "rePassword": "",
        "Email": "",
        "emailRules": [
            v => !!v || "E-mail is required",
            v => /.+@.+\..+/.test(v) || "E-mail must be valid",
        ],
        "checkbox": false,
        "role" : "学生",
        "options" : ["管理员", "教师", "学生"]
    }),

    "methods": {
        postCreate() {
          // console.log(this.role, this.options, this.options.indexOf(this.role))
          this.$api({
            "method": "POST",
            "url": "api/user",
            "data": {
              identity: this.options.indexOf(this.role),
              id: this.id,
              name: this.name,
              college: this.college,
              pwd: this.password,
              mail: this.Email
            },
          }).then(res => {
            console.log("注册", res);
            if (res.status === 200) {

              alert("注册成功，正在前往登录界面");
              this.$router.push({ "path": "/login" });

            } else if (res.status === 0) {
              alert(res.message)
              // this.clear()
            }

          });
        },
        Register () {
          this.$refs.form.validate()
          .then(success => {
            if (success) {
              this.postCreate()
            }
          })

        },
        clear () {

            this.id = "";
            this.password = "";
            this.rePassword = "";
            this.Email = "";

        },
        affirmPass (val) {

            if (val !== this.password) {

                return "两次密码不一致";

            }
            return true;

        },
    },
};
</script>

<style>
.login {
  background-image: url('../assets/bg1.jpeg');
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
#logo {
  position: relative;
  bottom: -20px;
}

.button {
  color: #596275;
  box-shadow: 9px 9px 18px rgba(0, 0, 0, 0.1),
  -9px -9px 18px rgba(255, 255, 255, 1);
  border-radius: 3rem;
  transition: box-shadow 0.2s ease-out;
  background-color: #efeeee;
  position: relative;
  top: 30px;
  margin-top: 20px;
  width: 130px;
  height: 55px;
  outline: none;
  border: none;
}
.login_ {
  font-size: 20px;
  margin-top: 15px;
}
.button:hover {
  font-size: 19px;
  box-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2),
  -1px -1px 2px rgba(255, 255, 255, 0.8);
  border-radius: 3rem;
  transition: box-shadow 0.2s ease-out;
  transition: font-size 0.2s ease-out;
}

.card {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  height: 650px;
  width: 550px;
  z-index: 1;
  transition: transform 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.card .front {
  position: absolute;
  text-align: center;
  box-shadow: 12px 12px 24px rgba(0, 0, 0, 0.1),
  -12px -12px 24px rgba(255, 255, 255, 1);
  border-radius: 3rem;
  background-color: #efeeee;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: 1s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}
.card .front {
  z-index: 1;
}
.return{
  top:40px;
}
</style>
