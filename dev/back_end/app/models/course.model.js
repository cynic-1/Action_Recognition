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
                enum: [1, 2] // autumn, spring
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
        },
        { timestamps: true }
    );
    // schema.method("toJSON", function() {
    //     const { __v, _id, ...object } = this.toObject();
    //     object.id = _id;
    //     return object;
    // });
    return mongoose.model("course", schema);
};
