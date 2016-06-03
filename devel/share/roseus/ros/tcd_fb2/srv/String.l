;; Auto-generated. Do not edit!


(when (boundp 'tcd_fb2::String)
  (if (not (find-package "TCD_FB2"))
    (make-package "TCD_FB2"))
  (shadow 'String (find-package "TCD_FB2")))
(unless (find-package "TCD_FB2::STRING")
  (make-package "TCD_FB2::STRING"))
(unless (find-package "TCD_FB2::STRINGREQUEST")
  (make-package "TCD_FB2::STRINGREQUEST"))
(unless (find-package "TCD_FB2::STRINGRESPONSE")
  (make-package "TCD_FB2::STRINGRESPONSE"))

(in-package "ROS")





(defclass tcd_fb2::StringRequest
  :super ros::object
  :slots (_exampleInput ))

(defmethod tcd_fb2::StringRequest
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

(defclass tcd_fb2::StringResponse
  :super ros::object
  :slots (_result ))

(defmethod tcd_fb2::StringResponse
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

(defclass tcd_fb2::String
  :super ros::object
  :slots ())

(setf (get tcd_fb2::String :md5sum-) "b8f71fbc3d8ee368e453fca947ab59d1")
(setf (get tcd_fb2::String :datatype-) "tcd_fb2/String")
(setf (get tcd_fb2::String :request) tcd_fb2::StringRequest)
(setf (get tcd_fb2::String :response) tcd_fb2::StringResponse)

(defmethod tcd_fb2::StringRequest
  (:response () (instance tcd_fb2::StringResponse :init)))

(setf (get tcd_fb2::StringRequest :md5sum-) "b8f71fbc3d8ee368e453fca947ab59d1")
(setf (get tcd_fb2::StringRequest :datatype-) "tcd_fb2/StringRequest")
(setf (get tcd_fb2::StringRequest :definition-)
      "string exampleInput
---
string result

")

(setf (get tcd_fb2::StringResponse :md5sum-) "b8f71fbc3d8ee368e453fca947ab59d1")
(setf (get tcd_fb2::StringResponse :datatype-) "tcd_fb2/StringResponse")
(setf (get tcd_fb2::StringResponse :definition-)
      "string exampleInput
---
string result

")



(provide :tcd_fb2/String "b8f71fbc3d8ee368e453fca947ab59d1")


