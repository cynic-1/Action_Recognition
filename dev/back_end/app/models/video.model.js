export default mongoose => {
    let schema = mongoose.Schema(
        {
            name: String,
            uploader: {
                type: mongoose.Schema.Types.ObjectId,
                ref: 'user'
            },
            raw: String, // file location
            processed: String, // file location
            keyPoints: [{
                type: mongoose.Schema.Types.ObjectId,
                ref: 'keyPoint'
            }]
        },
        { timestamps: true }
    );
    return mongoose.model("Video", schema);
};
