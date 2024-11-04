import express from "express";
import cors from "cors";
import cookieParser from "cookie-parser";
import { MAX_LIMIT_OF_DATA, STORE_STATIC_DATA } from "./constants.js";

const app = express();
app.use(cors({ origin: process.env.CORS_ORIGIN, credentials: true }));

app.use(express.json({ limit: `${MAX_LIMIT_OF_DATA}` })); //accept data : json format
app.use(express.urlencoded({ extended: true, limit: `${MAX_LIMIT_OF_DATA}` })); //accept data : url
app.use(express.static(`${STORE_STATIC_DATA}`)); //store  static data  in public folder.
app.use(cookieParser());

//routes import
import userRouter from "./routes/user.js";

//routes declaration
app.use("/users", userRouter);


export { app };
