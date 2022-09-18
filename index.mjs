#! /usr/bin/env node
import chalk from 'chalk';
import { createSpinner } from "nanospinner";
import { exec } from "child_process";
import { exit } from 'process';
import { appendFile, writeFileSync, appendFileSync } from 'fs';
import inquirer from "inquirer";

const python = '"C:\\Users\\Matheus\\Desktop\\github\\java tester\\index.py"'
const testsTemplate = (motivation, input, output) => {
    return `        {
            "motivation":"${motivation}",
            "input": "${input}",
            "output": "${output}"
        }`
} 

function textTemplate (name){
    return `Minimal test set for ${name}

AUTHORS:
- Matheus Tran 1777513`
}

var testCase = 0

function testCaseTemplate (input, output, motivation){
    testCase++
    return `

TEST CASE ${testCase}
motivation  : ${motivation}
input       : ${input}
output      : ${output}
`
}

exec("type minimal_test_set.json", async (error, stdout, stderr) => {
    if (stderr) {
        console.log(chalk.red('could not find "minimal_test_set.json" in cwd'))
        const input = await inquirer.prompt({
            name:"choice",
            type:"list",
            message:"Create file?\n",
            choices:[
                "yes",
                "no"
            ]
        })
        if (input.choice == "no"){
            exit()
        }
        console.log("creating file")
        const name = await inquirer.prompt({
            name:"name",
            type:"input",
            message:"file name: "
        })

        writeFileSync("minimal_test_set.json", `{\n    "file": "${name.name.replace(".java", "")}.java",\n    "tests": [\n`, err=>{})

        while (true) {
            const input = await inquirer.prompt([
                {name:"motivation", type:"input", message:"motivation: "},
                {name:"input", type:"input", message:"input: "},
                {name:"output", type:"input", message:"expected: "}
            ])
            appendFile("minimal_test_set.json", testsTemplate(input.motivation, input.input, input.output), err=>{})
            const exit = await inquirer.prompt({
                name:"exit",
                type:"list",
                message:"write test case?\n",
                choices:[
                    "yes",
                    "no"
                ]
            })
            if (exit.exit == "no"){
                appendFileSync("minimal_test_set.json", "\n    ]\n}", err=>{})
                break
            }
            appendFile("minimal_test_set.json", ",\n", err=>{})
        }
        exit()  
    } 
    const testSet = JSON.parse(stdout); 
    const spinner = createSpinner(`compiling ${testSet.file}`).start()
    exec(`javac ${testSet.file}`, (error, stdout, stderr) => {
        if (stderr) {
            spinner.error({text:chalk.red("failed to compile")})
            console.log(error)
            exit()
        }
        spinner.success({text:chalk.green("successfully compiled")})
        const testing = createSpinner(`running tests`).start()
        writeFileSync("minimal_test_set.txt", textTemplate(testSet.file), err=>{})
        testSet.tests.forEach((x) => {
            exec(`${python} ${testSet.file} "${x.input}"`, (error, stdout, stderr) => {
                if (stderr) {
                    testing.error({text:chalk.red("error occured")})
                    appendFile("minimal_test_set.txt", testCaseTemplate(x.input, "error", x.motivation), err=>{})
                } else {
                    const output = stdout.replaceAll(/[\n\r \t]+$/g, "")
                    appendFile("minimal_test_set.txt", testCaseTemplate(x.input, output, x.motivation), err=>{})
                    if (output === x.output) {
                        testing.success({text:chalk.green(`"${x.motivation}" passed`)})
                    } else {
                        testing.error({text:chalk.red(`"${x.motivation}" failed. expected: ${x.output}; got: ${output};`)})
                    }
                }
            })
        });
    })
    
})
