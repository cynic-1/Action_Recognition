export default mongoose => {
    let schema = mongoose.Schema(
        {
            imgLoc: String, // file location
            data: {
                upper: {
                    hitPosition: String,
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
                    }
                },
                ball: {
                    lastHeight: {
                        type: Number
                    },
                    initialAngle: {
                        type: Number,
                        min: 0,
                        max: 180
                    }
                },
                coordination: {
                    type: Number,
                    min: 0,
                    max: 100
                },
                rate: {
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
