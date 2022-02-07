export default mongoose => {
    let schema = mongoose.Schema(
        {
            name: String,
            raw: String, // file location
            processed: String, // file location
        },
        { timestamps: true }
    );
    // schema.method("toJSON", function() {
    //     const { __v, _id, ...object } = this.toObject();
    //     object.id = _id;
    //     return object;
    // });
    return mongoose.model("Video", schema);
};
