FROM golang:1.21-alpine AS build
WORKDIR /src
COPY . .
RUN apk add --no-cache git
RUN go build -o /bin/server ./cmd/server


FROM alpine:3.18
COPY --from=build /bin/server /bin/server
COPY .env.example /app/.env
WORKDIR /app
EXPOSE 8080
CMD ["/bin/server"]