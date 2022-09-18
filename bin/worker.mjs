import { spawn } from "child_process";

const args = process.argv

var worker = spawn("JAVA", [args[2]])

worker.stdin.write(args[3])
worker.stdin.end()

worker.stdout.on("data", (data) =>{
    console.log(data.toString())
})