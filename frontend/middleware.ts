import { clerkMiddleware } from "@clerk/nextjs/server";

const publicPathPrefixes = [
  "/",
  "/demo",
  "/sign-in",
  "/sign-up",
  "/login",
  "/api/health",
];

function isPublic(path: string): boolean {
  if (path === "/") return true;
  return publicPathPrefixes.some((prefix) => prefix !== "/" && path.startsWith(prefix));
}

export default clerkMiddleware(async (auth, request) => {
  if (!isPublic(request.nextUrl.pathname)) {
    await auth.protect();
  }
});

export const config = {
  matcher: [
    // Skip Next.js internals and all static files, unless found in search params
    "/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)",
    // Always run for API routes
    "/(api|trpc)(.*)",
    "/__clerk/:path*",
  ],
};
