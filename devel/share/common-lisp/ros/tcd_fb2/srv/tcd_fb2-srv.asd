
(cl:in-package :asdf)

(defsystem "tcd_fb2-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "String" :depends-on ("_package_String"))
    (:file "_package_String" :depends-on ("_package"))
  ))