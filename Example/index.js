#!/usr/bin / env node

import { exec, spawn } from "child_process";

const JAVA = "java";
const TEST_SET = "minimal_test_set.json";

const PROGRAM = "Cool.java";

function runJava(fileName, input, callback) {
    let worker = spawn(JAVA, [fileName]);
    worker.stdin.write(input);
    worker.stdin.end();
    worker.stdout.on('data', data => { callback(data.toString()) });
}

exec("type " + TEST_SET, (error, stdout, stderr) => {
    const testSet = JSON.parse(stdout);
    testSet.tests.forEach(t => {

        runJava(PROGRAM, t.input, (result) => {
            let success = t.expected == result;
            console.log(`input: ${t.input} | result: ${result} | success: ${success} | expected: ${t.expected}\n`);
        });

    });
});