export default mongoose => {
    let schema = mongoose.Schema(
        {
            identity: {
                type: Number,
                required: true,
                enum: [0, 1, 2] // adm; teacher; student
            },
            id: {
                type: String,
                required: true,
                index: true,
                unique: true,
                max: 20
            },
            name: {
                type: String,
                required: true,
                max: 20
            },
            college: {
                type: Number,
                enum: [1,2,3,4,5,6,7,8,9,10,
                11,12,13,14,15,16,17,18,19,20,
                21,22,23,24,25,26,27,28,29,30,
                31,32,33,34,35,36,37,38,39,40,
                41,42,44,48,49,50]
            },
            videos: [{
                type: mongoose.Schema.Types.ObjectId,
                ref: 'Video'
            }],
            mail: String,
            pwd: {
                type: String,
                required: true
            },
            courses: [{
                type: mongoose.Schema.Types.ObjectId,
                ref: 'course'
            }]
        },
    );
    // schema.method("toJSON", function() {
    //     const { __v, _id, ...object } = this.toObject();
    //     object.id = _id;
    //     return object;
    // });
    return mongoose.model("user", schema);
};
