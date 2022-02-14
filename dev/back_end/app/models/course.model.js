import integerValidator from 'mongoose-integer'
export default mongoose => {
    let schema = mongoose.Schema(
        {
            year: {
                type: Number,
                required: true,
            },
            semester: {
                type: Number,
                required: true,
                integer: true,
                enum: [1, 2] // autumn, spring
            },
            courseTime: {
                day: {
                    type: Number,
                    required: true,
                    integer: true,
                    min: 1,
                    max: 7
                },
                class: {
                    type: Number,
                    required: true,
                    integer: true,
                    min: 1,
                    max: 9
                }
            },
            name: {
                type: String, // e.g. volleyball
                required: true,
                max: 20
            },
            teachers: [{
                type: mongoose.Schema.Types.ObjectId,
                required: true,
                ref: "user"
            }],
            students: [{
                type: mongoose.Schema.Types.ObjectId,
                required: true,
                ref: "user"
            }],
            lessons: [{
                week: {
                    type: Number,
                    required: true,
                    integer: true,
                    min: 1,
                    max: 18
                },
                videos: [{
                    type: mongoose.Schema.Types.ObjectId,
                    ref: "video"
                }]
            }]
        },
    );
    // schema.method("toJSON", function() {
    //     const { __v, _id, ...object } = this.toObject();
    //     object.id = _id;
    //     return object;
    // });
    schema.plugin(integerValidator);
    return mongoose.model("course", schema);
};
