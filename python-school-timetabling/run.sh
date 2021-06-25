#!/bin/sh
PROGRAM=${GRAALVM_HOME}/bin/graalpython
CLASSPATH=target/classes:`cat target/java.classpath`
$PROGRAM --polyglot --jvm --vm.cp=$CLASSPATH src/main/resources/python/main.py
