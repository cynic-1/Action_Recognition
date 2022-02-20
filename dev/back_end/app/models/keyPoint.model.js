export default mongoose => {
    let schema = mongoose.Schema(
        {
            imgLoc: String, // file location
            data: {
                upper: {
                    hitPosition: String, // 击球部位
                    hitAngle: { // 小臂与水平方向夹角
                        type: Number,
                        min: 0,
                        max: 180
                    },
                    angleForearmArm: { // 小臂与大臂夹角
                        type: Number,
                        min: 0,
                        max: 180
                    },
                    angleArmTrunk: { // 大臂与躯干夹角
                        type: Number,
                        min: 0,
                        max: 180
                    }
                },
                lower: {
                    angleCalfThigh: { // 小腿与大腿夹角
                        type: Number,
                        min: 0,
                        max: 180
                    },
                    angleThighTrunk: { // 大腿与躯干夹角
                        type: Number,
                        min: 0,
                        max: 180
                    },
                    jumpHeight: {
                        type: Number,
                        min: 0
                    }
                },
                ball: {
                    lastHeight: { // 上次击球至今的球最大高度
                        type: Number
                    },
                    initialAngle: { // 初速度方向与水平夹角
                        type: Number,
                        min: 0,
                        max: 180
                    },
                    initialVelocity: { // 初速度 (m/s)
                        type: Number,
                        min: 0
                    }
                },
                coordination: { // 协调性得分
                    type: Number,
                    min: 0,
                    max: 100
                },
                accuracy: { // 准确性得分
                    type: Number,
                    min: 0,
                    max: 100
                },
                rate: { // 该动作总得分
                    type: Number,
                    min: 0,
                    max: 180
                }
            }
        },
        // { timestamps: true }
    );
    // schema.method("toJSON", function() {
    //     const { __v, _id, ...object } = this.toObject();
    //     object.id = _id;
    //     return object;
    // });
    return mongoose.model("keyPoint", schema);
};
