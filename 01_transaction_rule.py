# Databricks notebook source
# Lab 5.1 baseline: edit the function only, then rerun the examples.
def normalize_transaction(value):
    return value

examples = [" Login ", "Search", " Checkout "]
for value in examples:
    print(repr(value), "->", repr(normalize_transaction(value)))
