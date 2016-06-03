;; Auto-generated. Do not edit!


(when (boundp 'template_sm::String)
  (if (not (find-package "TEMPLATE_SM"))
    (make-package "TEMPLATE_SM"))
  (shadow 'String (find-package "TEMPLATE_SM")))
(unless (find-package "TEMPLATE_SM::STRING")
  (make-package "TEMPLATE_SM::STRING"))
(unless (find-package "TEMPLATE_SM::STRINGREQUEST")
  (make-package "TEMPLATE_SM::STRINGREQUEST"))
(unless (find-package "TEMPLATE_SM::STRINGRESPONSE")
  (make-package "TEMPLATE_SM::STRINGRESPONSE"))

(in-package "ROS")





(defclass template_sm::StringRequest
  :super ros::object
  :slots (_exampleInput ))

(defmethod template_sm::StringRequest
  (:init
   (&key
    ((:exampleInput __exampleInput) "")
    )
   (send-super :init)
   (setq _exampleInput (string __exampleInput))
   self)
  (:exampleInput
   (&optional __exampleInput)
   (if __exampleInput (setq _exampleInput __exampleInput)) _exampleInput)
  (:serialization-length
   ()
   (+
    ;; string _exampleInput
    4 (length _exampleInput)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _exampleInput
       (write-long (length _exampleInput) s) (princ _exampleInput s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _exampleInput
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _exampleInput (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass template_sm::StringResponse
  :super ros::object
  :slots (_result ))

(defmethod template_sm::StringResponse
  (:init
   (&key
    ((:result __result) "")
    )
   (send-super :init)
   (setq _result (string __result))
   self)
  (:result
   (&optional __result)
   (if __result (setq _result __result)) _result)
  (:serialization-length
   ()
   (+
    ;; string _result
    4 (length _result)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _result
       (write-long (length _result) s) (princ _result s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _result
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _result (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass template_sm::String
  :super ros::object
  :slots ())

(setf (get template_sm::String :md5sum-) "b8f71fbc3d8ee368e453fca947ab59d1")
(setf (get template_sm::String :datatype-) "template_sm/String")
(setf (get template_sm::String :request) template_sm::StringRequest)
(setf (get template_sm::String :response) template_sm::StringResponse)

(defmethod template_sm::StringRequest
  (:response () (instance template_sm::StringResponse :init)))

(setf (get template_sm::StringRequest :md5sum-) "b8f71fbc3d8ee368e453fca947ab59d1")
(setf (get template_sm::StringRequest :datatype-) "template_sm/StringRequest")
(setf (get template_sm::StringRequest :definition-)
      "string exampleInput
---
string result

")

(setf (get template_sm::StringResponse :md5sum-) "b8f71fbc3d8ee368e453fca947ab59d1")
(setf (get template_sm::StringResponse :datatype-) "template_sm/StringResponse")
(setf (get template_sm::StringResponse :definition-)
      "string exampleInput
---
string result

")



(provide :template_sm/String "b8f71fbc3d8ee368e453fca947ab59d1")


