# Makefile for source rpm: gstreamer
# $Id$
NAME := gstreamer
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
