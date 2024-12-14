import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/sandbox")({
  component: RouteComponent,
});

function RouteComponent() {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">Sandbox</h1>
      <p>
        Upload and run compiled binaries to benchmark them to diff with previous
        versions
      </p>
      <form className="flex flex-col gap-4 mt-4">
        {/* submit files and textarea for command script to run*/}
        <Input type="file" />
        <Textarea
          placeholder="#!/bin/sh
./testbin"
          className="h-64"
        />
        <Button type="submit">Run</Button>
      </form>
    </div>
  );
}
