export default () => ({
  googleApi: {
    clientEmail: process.env.GOOGLE_CLIENT_EMAIL,
    privateKey: process.env.GOOGLE_PRIVATE_KEY?.replace(/\\n/g, '\n'), // optional fix for multiline keys,
    projectId: process.env.GOOGLE_PROJECT_ID,
  },
});
