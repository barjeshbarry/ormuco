if(WANT_INSTALLER)
    set(python_files
        NetworkUtil.py
        __init__.py
    )
    install( FILES ${python_files} DESTINATION lib/python/site-packages/appFrameworkPython/NetworkUtil )
endif()

