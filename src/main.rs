use axum::Router;
use tower_http::services::ServeDir;

#[tokio::main]
async fn main() {
    // define routes
    let app = Router::new()
        .nest_service("/", ServeDir::new("static"));

    // bind & serve
    let listener = tokio::net::TcpListener::bind("0.0.0.0:8080")
        .await
        .unwrap();
    axum::serve(listener, app).await.unwrap();
}
