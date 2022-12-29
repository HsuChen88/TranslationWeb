def image_ocr(read_image_url):
    from azure.cognitiveservices.vision.computervision import ComputerVisionClient
    from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
    from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
    from azure.cognitiveservices.vision.computervision.models import ComputerVisionOcrErrorException
    from msrest.authentication import CognitiveServicesCredentials

    import time

    subscription_key = "f94c32d1a8414aaf99dd206bf590c324"
    endpoint = "https://test0258.cognitiveservices.azure.com/"

    try:
        computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

        '''
        OCR: Read File using the Read API, extract text - remote
        This example will extract text in an image, then print results, line by line.
        This API call can also extract handwriting style text (not shown).
        '''
        print("===== Read Image - remote =====")
        # Get an image with text

        # Call API with URL and raw response (allows you to get the operation location)
        read_response = computervision_client.read(read_image_url,  raw=True) 

        # Get the operation location (URL with an ID at the end) from the response
        read_operation_location = read_response.headers["Operation-Location"]
        # Grab the ID from the URL
        operation_id = read_operation_location.split("/")[-1]

        # Call the "GET" API and wait for it to retrieve the results 
        while True:
            read_result = computervision_client.get_read_result(operation_id)
            if read_result.status not in ['notStarted', 'running']:
                break
            time.sleep(1)

        # Print the detected text, line by line
        text = ""
        if read_result.status == OperationStatusCodes.succeeded:
            for text_result in read_result.analyze_result.read_results:
                for line in text_result.lines:
                    text += line.text + "\n"
        print("END - Read File - remote")
        return text
    except ComputerVisionOcrErrorException:
        return "The type of image could not be understood."
        
    '''
    END - Read File - remote
    '''
