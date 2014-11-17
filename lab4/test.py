import tweetpony

class StreamProcessor(tweetpony.StreamProcessor):
    def on_status(self, status):
        print "%s: %s" % (status.user.screen_name, status.text)
        return True

try:
    api = tweetpony.API("sqjwOmPIc6qfOPR2YVIKTXfMz",
                        "2imj49S2Z0ZWdXc5Nm6nAChEjLa42nLncTnIcnJBBwva2ldLNf",
                        "2902918832-x5y3tFlt2zhbf9u2SLW2uJO289TFSUslxdxemx8",
                        "AqA784KdlzCyGSqeUrz7VlV7ZmrDFKU3krA0ATaqPtcl0")
except tweetpony.APIError as err:
    print(err.code, err.description)

processor = StreamProcessor(api)
try:
    api.user_stream(processor = processor)
except KeyboardInterrupt:
    pass


