build_dir ?= ./build
src_dir ?= .
prefix ?= $(HOME)/Library/Application\ Scripts/com.devon-technologies.think3
install_dir ?= Dynalist2MD
install_path_menu := $(prefix)/Menu/$(install_dir)
install_path_toolbar := $(prefix)/Toolbar

srcs := $(shell find $(src_dir) -name '*.jxa')
execs := $(srcs:%.jxa=$(build_dir)/%.scpt)

all: $(execs)

$(build_dir)/%.scpt: %.jxa | $(build_dir)
	@echo Compiling $<
	@osacompile -l JavaScript -o $@ $<

$(build_dir):
	@$(MKDIR_P) -p $@

install_menu: $(execs) | $(prefix)
	@echo Installing all scripts to Menu: $(install_path_menu)
	@install -d $(install_path_menu)
	@install -m 644 $(execs) $(install_path_menu)

install_toolbar:  # install one script to toolbar at a time
	@scpt=$(firstword $(filter-out $@, $(MAKECMDGOALS))).scpt; \
	scpt_path="$(build_dir)/$$scpt"; \
	if ! test -f "$$scpt_path"; then \
	  echo >&2 "$$scpt_path": No such script, you might need to compile first.; \
	  exit 1; \
	fi; \
	echo Installing "$$scpt" to Toolbar: $(install_path_toolbar); \
	install -d $(install_path_toolbar); \
	install -m 644 "$$scpt_path" $(install_path_toolbar)

%:
	@:

$(prefix):
	@if ! test -d $(prefix); then \
		echo >&2 prefix dir does not exist. && exit 1; \
	fi; \

uninstall_menu:
	@echo Removing all scripts from Menu: $(install_path_menu)
	@$(RM) -r $(install_path_menu)

uninstall_toolbar:
	@for i in $(execs); do \
	  scpt_name="$$(basename $$i)"; \
	  scpt_path=$(install_path_toolbar)/"$$scpt_name"; \
	  if test -f "$$scpt_path"; then \
	    echo Removing from Toolbar: $$scpt_path; \
	    $(RM) "$$scpt_path"; \
	  fi; \
	done

clean:
	@$(RM) -r $(build_dir)

.PHONY: clean all install

MKDIR_P := mkdir -p
