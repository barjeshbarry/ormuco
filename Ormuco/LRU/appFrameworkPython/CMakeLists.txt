add_subdirectory(Application)
add_subdirectory(Logger)
add_subdirectory(NetworkUtil)

set(python_files
    __init__.py
)

if(WANT_INSTALLER)
    install( FILES ${python_files} DESTINATION lib/python/site-packages/appFrameworkPython )
endif()


