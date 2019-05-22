# Nested Comment Threads built with AWS Serverless

More info here: https://coderecipe.ai/architectures/51056928

## Prerequisites
```  
npm install serverless  
```  
Make sure you have AWS access key and secrete keys setup locally, following this video [here](https://www.youtube.com/watch?v=KngM5bfpttA)

## Download the code locally

```  
serverless create --template-url http://github.com/codeRecipe-dev/nested-comments-serverless --path nested-comments-serverless
```

## Deploy to the cloud  

```
cd nested-comments-serverless

npm install

serverless deploy --stage <your-stage-name>
```

**DynamoDB Sample**

![Table](https://s3.amazonaws.com/coderecipe-crlite-architectures-beta/Rohit/Nested+Comment+Threads+in+AWS+Serverless/table_preview.png)

**Frontend Preview**

![Preview](https://s3.amazonaws.com/coderecipe-crlite-architectures-beta/Rohit/Nested+Comment+Threads+in+AWS+Serverless/comments_preview.jpg)
