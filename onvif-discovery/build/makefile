.PHONY: buildImageAmd64 buildImageArm64 restart

buildImageAmd64:
	docker build -f ./dockerfile-sum/amd64 --tag onvif-discovery-amd64:1.0 .

buildImageArm64:
	docker build -f ./dockerfile-sum/arm64 --tag onvif-discovery-arm64:1.0 .
