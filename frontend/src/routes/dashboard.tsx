import { createFileRoute } from "@tanstack/react-router";
import { Link } from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

// import Image from "next/image";
import { AspectRatio } from "@/components/ui/aspect-ratio";
// import { API_URL } from "@/lib/utils";
import { getCommits, getRepos, getUser } from "@/lib/api";

export const Route = createFileRoute("/dashboard")({
  component: RouteComponent,
});

function RouteComponent() {
  const [user, setUser] = useState([]);
  const [repos, setRepos] = useState([]);
  const [selectedRepo, setSelectedRepo] = useState("");
  const [selectedBranch, setSelectedBranch] = useState("");
  const [commits, setCommits] = useState([]);
  const [ tableLoading, setTableLoading ] = useState(true);

  useEffect(() => {
    async function fetchUser() {
      const data = await getUser();
      setUser(data);
    }
    fetchUser();
    async function fetchRepo() {
      const data = await getRepos();
      setRepos(data);
    }
    fetchRepo();
    async function getLoader() {
      const { bouncy } = await import("ldrs");
      bouncy.register();
    }
    getLoader();
  }, []);

  useEffect(() => {
    setTableLoading(true);
    async function fetchCommits() {
      const data = await getCommits(selectedRepo, selectedBranch);
      setCommits(data);
      setTableLoading(false);
    }
    fetchCommits();
  }, [selectedBranch]);

  return (
    <div className="flex">
      {/* nav bar */}
      <div className="py-7 px-4 flex flex-col justify-between max-h-screen h-screen w-64 dark:bg-stone-950">
        <div className="flex flex-col gap-4 text-wrap">
          <div className="flex gap-4 items-center">
            <img
              src={`${user.avatar_url}`}
              alt="User Avatar"
              className="object-cover w-10 h-10 rounded-full"
            />
            <h1 className="font-bold text-wrap">{user.username}</h1>
          </div>
          <div>
            <h1 className="text-stone-400">Repositories</h1>

            <Accordion
              type="single"
              collapsible
              className="max-h-[calc(100vh-8rem)] overflow-y-auto"
            >
              {repos.map((repo) => {
                return (
                  <AccordionItem value={repo.name}>
                    <AccordionTrigger className="">
                      {repo.name}
                    </AccordionTrigger>
                    <AccordionContent className="max-h-96 overflow-y-auto overflow-x-hidden">
                      <div className="flex flex-col gap-1">
                        {repo.branches.map((branch) => {
                          return (
                            <Button
                              className="text-black w-full px-2 text-left overflow-ellipsis whitespace-nowrap bg-slate-200 hover:text-white hover:bg-slate-500"
                              onClick={() => {
                                setSelectedRepo(repo.name);
                                setSelectedBranch(branch.name);
                              }}
                            >
                              {branch.name}
                            </Button>
                          );
                        })}
                      </div>
                    </AccordionContent>
                  </AccordionItem>
                );
              })}
            </Accordion>
          </div>
        </div>
        <div className="flex flex-col gap-2">
          <p className="">Selected Repo: {selectedRepo}</p>
          <p className="">Selected Branch: {selectedBranch}</p>
          <Button asChild variant="destructive">
            <Link href="/logout">Logout</Link>
          </Button>
        </div>
      </div>
      {/* body content */}
      <div className="bg-slate-100 dark:bg-stone-900 max-w-screen h-screen flex-grow p-4">
        {tableLoading ? (
          <l-bouncy size="30" speed="1.75" color="#595cff"></l-bouncy>
        ) : (
          <Table className="w-full h-96">
            <TableCaption>Commits</TableCaption>
            <TableHeader>
              <TableRow className="w-full">
                <TableHead className="w-[100px]">Commit</TableHead>
                <TableHead>Author</TableHead>
                <TableHead>Date</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {commits.map((commit) => {
                return (
                  <TableRow key={commit.sha}>
                    <TableCell>{commit.commit.message}</TableCell>
                    <TableCell>{commit.commit.author.name}</TableCell>
                    <TableCell>{commit.commit.author.date}</TableCell>
                    <TableCell>
                      <Button variant="secondary">Scan</Button>
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        )}
      </div>
    </div>
  );
}
