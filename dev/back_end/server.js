import express from 'express'
import bodyParser from "body-parser"
import cors from 'cors'
import db from './app/models/index.js'
import userRoutes from "./app/routes/user.routes.js";
import videoRoutes from "./app/routes/video.routes.js";
import courseRoutes from "./app/routes/course.routes.js";
// import fs from 'fs'

const app = express();

const corsOptions = {
    origin: "http://localhost:8080"
};

app.use(cors(corsOptions));

// parse requests of content-type - application/json
app.use(bodyParser.json());

// parse requests of content-type - application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: true }));

// simple route
app.get("/", (req, res) => {
    res.json({ message: "Welcome to bezkoder application." });
});

userRoutes(app);
videoRoutes(app);
courseRoutes(app);
// set port, listen for requests
const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}.`);
});

db.mongoose
    .connect(db.url, {
        useNewUrlParser: true,
        useUnifiedTopology: true
    })
    .then(() => {
        console.log("Connected to the database!");
    })
    .catch(err => {
        console.log("Cannot connect to the database!", err);
        process.exit();
    });
