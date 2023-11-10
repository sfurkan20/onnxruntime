#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import argparse
import os
import pathlib


def CheckDelegateUnmanagedFunctionPointerMatch(file: pathlib.Path):
    """
    Check that all 'public delegate' declarations have a matching UnmanagedFunctionPointer attribute.
    Check is very simplistic and does not take into account comments.
    :param file: C# source file to check.
    :return: Number of errors
    """

    print(f"Checking {str(file)}")

    errors = 0
    line_num = 0
    with open(str(file.resolve(strict=True))) as f:
        prev_line = ""
        for line in f.readlines():
            line_num += 1

            # strip so it's easier to deal with commented out lines.
            line = line.strip()
            if line.startswith("public delegate ") and not prev_line.startswith("[UnmanagedFunctionPointer"):
                errors += 1
                print(f"Line {line_num} is missing UnmanagedFunctionPointer attribute:\n\t{prev_line}\n\t{line}")

            prev_line = line

    return errors


def main():
    arg_parser = argparse.ArgumentParser(
        "Script to validate that the native delegates for the ONNX Runtime C# managed projects have the required "
        "attributes for iOS AOT. Paths are inferred from the script location."
        "Errors of this nature can only be detected at runtime, in a release build, of a Xamarin/MAUI app, "
        "on an actual iOS device. Due to that we take extra steps to identify problems early."
    )

    # no real arg. just using this to provide description as help message
    _ = arg_parser.parse_args()

    script_dir = pathlib.Path(__file__).parent
    csharp_root = script_dir.parent
    print(f"__file__: {__file__}")
    print(f"Script dir: {script_dir}")

    managed_dir = csharp_root / "src" / "Microsoft.ML.OnnxRuntime"
    native_methods =  managed_dir / "NativeMethods.shared.cs"
    training_native_methods = managed_dir / "Training" / "NativeTrainingMethods.shared.cs"
    errors = CheckDelegateUnmanagedFunctionPointerMatch(native_methods)
    errors += CheckDelegateUnmanagedFunctionPointerMatch(training_native_methods)

    if errors:
        raise ValueError(f"{errors} errors were found. Please check output for specifics.")


if __name__ == "__main__":
    main()