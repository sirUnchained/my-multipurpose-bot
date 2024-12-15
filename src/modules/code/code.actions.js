const path = require("node:path");
const fs = require("node:fs");
const child_process = require("node:child_process");
const { Markup } = require("telegraf");

const actionsDB = require("./../../databases/controllers/actions.controller");
const usersDb = require("./../../databases/controllers/users.controller");

const watingList = new Set();

const compileCode = async (ctx) => {
  const chatId = ctx.chat.id;
  const user = usersDb.findOne("chatId", chatId);
  if (watingList.has(chatId) && user.role !== "admin") {
    await ctx.reply("لطفا 20 ثانیه دیگر دوباره امتحان کنید.");
    return;
  }

  const action = actionsDB.findOne("chatId", chatId);
  const untrustedCode = ctx.message.text;
  let result = null;
  switch (true) {
    case action.code_with === "py":
      result = await compilePython(untrustedCode);
      result = result?.replaceAll(/app\/src\/modules\/code\/temp(code*)?/g, "");
      await ctx.replyWithMarkdownV2(`\`${result}\``);
      break;
    case action.code_with === "cpp":
      result = await compileCplusplus(untrustedCode);
      result = result?.replaceAll(/app\/src\/modules\/code\/temp(code*)?/g, "");
      await ctx.replyWithMarkdownV2(`\`${result}\``);
      break;
    case action.code_with === "js":
      result = await compileJavaScript(untrustedCode);
      result = result?.replaceAll(/app\/src\/modules\/code\/temp(code*)?/g, "");
      await ctx.replyWithMarkdownV2(`\`${result}\``);
      break;
    default:
      await ctx.reply("فکر کنم مشکلی پیش اومده.");
      break;
  }

  setTimeout(() => {
    watingList.delete(chatId);
  }, 20 * 1000);
};
async function compilePython(userCode) {
  const codeFile = path.join(__dirname, "temp", "code.py");
  const trustedCode = userCode
    .replaceAll(/import.*/g, "")
    .replaceAll(/from.*/g, "");

  const preModules = "import copy\nimport random\n";

  fs.writeFileSync(codeFile, preModules + trustedCode);

  try {
    const result = child_process.execSync(`python3 ${codeFile}`, {
      timeout: 5000,
      maxBuffer: 4090,
    });
    fs.unlinkSync(codeFile);
    return result.toString().trim() || "بدون خروجی.";
  } catch (err) {
    fs.unlinkSync(codeFile);
    return (
      err.stderr?.toString().split("\n").slice(1, 5).join("\n") ||
      "خطای ناشناخته\n احتمالا خروجی کد بیش از حد بزرگ بوده.\n"
    );
  }
}
async function compileCplusplus(userCode) {
  const codeFile = path.join(__dirname, "temp", "code.cpp");
  const trustedCode = userCode.replaceAll(/#include.*/g, "");

  const neededLibs =
    "#include<iostream>\n#include<cmath>\n#include<array>\n#include<vector>\n#include<algorithm>\n";
  fs.writeFileSync(codeFile, `${neededLibs + trustedCode}`);

  try {
    child_process.execSync(
      `g++ -o ${path.join(__dirname)}/temp/compiled.exe ${codeFile}`,
      {
        timeout: 5000,
      }
    );
    fs.unlinkSync(codeFile);
  } catch (err) {
    fs.unlinkSync(codeFile);
    return (
      err.stderr?.toString().split("\n").slice(1, 5).join("\n") ||
      "خطایی ناشناخته در زمان کامپایل رخ داد."
    );
  }

  const compiledFile = path.join(__dirname, "temp", "compiled.exe");
  try {
    const result = child_process.execSync(`${compiledFile}`, {
      timeout: 5000,
      maxBuffer: 4090,
    });
    fs.unlinkSync(compiledFile);
    return result.toString().trim() || "بدون خروجی.";
  } catch (err) {
    fs.unlinkSync(compiledFile);
    return (
      err.stderr?.toString().split("\n").slice(1, 5).join("\n") ||
      "خطای ناشناخته\n احتمالا خروجی کد بیش از حد بزرگ بوده.\n"
    );
  }
}
async function compileJavaScript(userCode) {
  const codeFile = path.join(__dirname, "temp", "code.js");
  const trustedCode = userCode
    .replaceAll(/import.*/g, "")
    .replaceAll(/from.*/g, "")
    .replaceAll("__dirname", "'👍'")
    .replaceAll("__filename", "'👍'")
    .replaceAll("require", "accessDenied")
    .replaceAll("module", "accessDenied");

  fs.writeFileSync(codeFile, trustedCode);

  try {
    const result = child_process.execSync(`node ${codeFile}`, {
      timeout: 5 * 1000,
      maxBuffer: 4090,
    });
    fs.unlinkSync(codeFile);
    return result.toString().trim() || "بدون خروجی.";
  } catch (err) {
    fs.unlinkSync(codeFile);
    return (
      err.stderr?.toString().split("\n").slice(1, 5).join("\n") ||
      "خطای ناشناخته\n احتمالا خروجی کد بیش از حد بزرگ بوده."
    );
  }
}

async function sendCompileLangs(ctx) {
  try {
    await ctx.editMessageText(
      "خب با چه زبانی کد زدی؟",
      Markup.inlineKeyboard([
        [
          Markup.button.callback("پایتون", "py"),
          Markup.button.callback("سی پلاس پلاس", "cpp"),
        ],
        [Markup.button.callback("جاوا اسکریپت", "js")],
        [Markup.button.callback("back", "back")],
      ])
    );
  } catch (error) {
    await ctx.reply(
      "خب با چه زبانی کد زدی؟",
      Markup.inlineKeyboard([
        [
          Markup.button.callback("پایتون", "py"),
          Markup.button.callback("سی پلاس پلاس", "cpp"),
        ],
        [Markup.button.callback("جاوا اسکریپت", "js")],
        [Markup.button.callback("back", "back")],
      ])
    );
  }
}

module.exports = { sendCompileLangs, compileCode };
