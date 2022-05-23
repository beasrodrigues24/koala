# Koal@ Manual

<p align="center">
<img src="logo.png" alt="logo" width="200" />
</p>

- [Koal@ Manual](#koal-manual)
  - [What is it?](#what-is-it)
  - [How to use it?](#how-to-use-it)
  - [Why is it useful?](#why-is-it-useful)
  - [Authors](#authors)
  - [Koal@ Syntax](#koal-syntax)
    - [Text](#text)
    - [Variables](#variables)
    - [Comments](#comments)
    - [Conditionals](#conditionals)
    - [Loops](#loops)
    - [Aliases](#aliases)
    - [Pipes](#pipes)
    - [Includes](#includes)

## What is it?

Koal@ is a template language inspired by the well known Pandoc Template Language. By receiving a template followed by defined syntax and a dictionary (YAML or JSON), it generates an output file with the desired extension.

## How to use it?

`python3 src/koala.py template -dt TYPE dictionary outputfile` where `TYPE` is `json` or `yaml`.

`python3 src/koala.py -h` shows the help menu.

## Why is it useful?

By defining a template, or using one of the pre-defined available on the [examples directory](https://github.com/beasrodrigues24/koala/tree/main/examples), the user can simplify the work of writing a document or a web page. 

This way, the user is capable of automating the generation of the desired files.

## Authors

Koal@ was created in the context of Language Processing class at University of Minho, Braga, Portugal.

It was the second practical assignment done by the following students:

[Beatriz Rodrigues](https://github.com/beasrodrigues24)

[Francisco Neves](https://github.com/franl08)

[Guilherme Fernandes](https://github.com/zer0-5)

## Koal@ Syntax

### Text

Inside double quotes (p.e. `"this is an example of text"`).

### Variables

* **Dictionary Variables**: Using `@` (p.e. `@variable`);
* **Temporary Variables**: Using `#` (p.e. `#tmp`)

### Comments

Using double slashes, just like C (p.e. `// this is a comment`).

### Conditionals

Using `if`, `elif` and `else`. For example:
```
if @var {
    "var exists"
} elif @var2{
    "var2 exists"
} else {
    "var and var2 doesn't exist"
}
```

### Loops

Using `for`. For example:
```
for #tmpvar : @vars {
    #tmpvar " is in vars."
}
```

### Aliases

Using `alias` prefix to define it or the name of the alias followed by `(arg1, arg2, ...)` to call it. For example:
```
// Defining
alias cd #dir {
    "cd " #dir
}
// Using
cd(@dir1)
```

### Pipes

Using `/` followed by the name of the desired pipe. The following pipes are available:

* **First**: Used with `/first` to get the first element of a list;
* **Last**: Used with `/last` to get the last element of a list;
* **Head**: Used with `/head` to get all the elements of a list except the last one;
* **Tail**: Used with `/tail` to get all the elements of a list except the first one;
* **Upper**: Used with `/upper` to convert a string to uppercase;
* **Lower**: Used with `/lower` to convert a string to lowercase;
* **Reverse**: Used with `/reverse` to reverse a string or a list.

For example:
```
for #name : @names/head{#name", "} @names/last
```
Will produce a list of the names at `@names` separated by a comma, except the last one.
```
for #name : @names{#name/upper" "}
```
Will produce a list of the names at `@names` in uppercase.
```
for #name : @names/reverse{#names" "}
```
Will produce a list of the names at `@names` in the reverse order.

### Includes

Used to import aliases from another `.koa` file (p.e. `include "file.koa"`). The path of the included file should be relative to the directory where the koal@ app will be run.
